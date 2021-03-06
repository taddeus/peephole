from src.statement import Statement as S
from src.liveness import RESERVED_REGISTERS, is_reg_dead_after
from src.dataflow import succ


def find_free_reg(block, start):
    """Find a temporary register that is free in a given list of statements."""
    for i in xrange(8, 16):
        tmp = '$%d' % i

        if is_reg_dead_after(tmp, block, start):
            return tmp

    raise Exception('No temporary register is available.')


def eliminate_common_subexpressions(block):
    """
    Common subexpression elimination:
    x = a + b           ->  u = a + b
    y = a + b               x = u
                            y = u

    The algorithm used is as follows:
    - Traverse through the statements.
    - If the statement can be possibly be eliminated, walk further collecting
      all other occurrences of the expression until one of the arguments is
      assigned in a statement, or the start of the block has been reached.
    - If one or more occurrences were changed, insert the expression with a new
      destination address before the last changed occurrence and change all
      occurrences to a move instruction from that address.
    """
    changed = False

    block.reset()

    while not block.end():
        s = block.read()

        if s.is_arith():
            pointer = block.pointer
            occurrences = [pointer - 1]
            args = s[1:]

            # Collect similar statements
            while not block.end():
                s2 = block.read()

                if not s2.is_command():
                    continue

                # Stop if one of the arguments is assigned
                if len(s2) and s2[0] in args:
                    break

                # Replace a similar expression by a move instruction
                if s2.name == s.name and s2[1:] == args:
                    occurrences.append(block.pointer - 1)

            if len(occurrences) > 1:
                new_reg = find_free_reg(block, occurrences[0])

                # Replace each occurrence with a move statement
                message = 'Common subexpression reference: %s %s' \
                        % (s.name, ','.join(map(str, [new_reg] + s[1:])))

                for occurrence in occurrences:
                    rd = block[occurrence][0]
                    block.replace(1, [S('command', 'move', rd, new_reg)], \
                            start=occurrence, message=message)

                # Insert the calculation before the original with the new
                # destination address
                message = 'Common subexpression: %s %s' \
                        % (s.name, ','.join(map(str, s)))
                block.insert(S('command', s.name, *([new_reg] + args)), \
                                index=occurrences[0], message=message)

                changed = True

            # Reset pointer to continue from the original statement
            block.pointer = pointer

    return changed


def to_hex(value):
    """Create the hexadecimal string of an integer."""
    return '0x%08x' % value


def fold_constants(block):
    """
    Constant folding:
    x = 3 + 5           ->  x = 8
    y = x * 2               y = 16

    Also preforms algebraic transformations:
    x = y + 0           ->  x = y
    etc.

    To keep track of constant values, the following assumptions are made:
    - An immediate load defines a register value:
        li $reg, XX     ->  register[$reg] = XX
    - Integer variable definition is of the following form:
        li $reg, XX     ->  constants[VAR] = XX
        sw $reg, VAR    ->  register[$reg] = XX
    - When a variable is used, the following happens:
        lw $reg, VAR    ->  register[$reg] = constants[VAR]
    """
    changed = False

    # Variable values
    constants = {}

    # Current known values in register
    register = {}

    block.reset()

    while not block.end():
        s = block.read()
        known = []

        if not s.is_command():
            continue

        if s.name == 'li':
            # Save value in register
            if not isinstance(s[1], int): # Negative numbers are stored as int
                register[s[0]] = int(s[1], 16)
            else:
                register[s[0]] = s[1]
            known.append((s[0], register[s[0]]))
        elif s.name == 'move' and s[0] in register:
            reg_to, reg_from = s

            if reg_from in register:
                # Other value is also known, copy its value
                register[reg_to] = register[reg_from]
                known.append((reg_to, register[reg_to]))
            else:
                # Other value is unknown, delete the value
                del register[reg_to]
                known.append((reg_to, 'unknown'))
        elif s.name == 'sw' and s[0] in register:
            # Constant variable definition, e.g. 'int a = 1;'
            constants[s[1]] = register[s[0]]
            known.append((s[1], register[s[0]]))
        elif s.name == 'lw' and s[1] in constants:
            # Usage of variable with constant value
            register[s[0]] = constants[s[1]]
            known.append((s[0], register[s[0]]))
        elif s.name == 'mflo' and '$lo' in register:
            # Move of `Lo' register to another register
            register[s[0]] = register['$lo']
            known.append((s[0], register[s[0]]))
        elif s.name == 'mfhi' and '$hi' in register:
            # Move of `Hi' register to another register
            register[s[0]] = register['$hi']
            known.append((s[0], register[s[0]]))
        elif s.name == 'mult' and s[0]in register and s[1] in register:
            # Multiplication/division with constants
            rs, rt = s
            a, b = register[rs], register[rt]

            if not a or not b:
                # Multiplication by 0
                hi = lo = to_hex(0)
                message = 'Multiplication by 0: %d * 0' % (b if a else a)
            elif a == 1:
                # Multiplication by 1
                hi = to_hex(0)
                lo = to_hex(b)
                message = 'Multiplication by 1: %d * 1' % b
            elif b == 1:
                # Multiplication by 1
                hi = to_hex(0)
                lo = to_hex(a)
                message = 'Multiplication by 1: %d * 1' % a
            else:
                # Calculate result and fill Hi/Lo registers
                result = a * b
                binary = bin(result)[2:]
                binary = '0' * (64 - len(binary)) + binary
                hi = int(binary[:32], base=2)
                lo = int(binary[32:], base=2)
                message = 'Constant multiplication: %d * %d = %d' \
                            % (a, b, result)

            # Replace the multiplication with two immidiate loads to the
            # Hi/Lo registers
            block.replace(1, [S('command', 'li', '$hi', hi),
                                S('command', 'li', '$lo', lo)],
                            message=message)

            register['$lo'], register['$hi'] = lo, hi
            known += [('$lo', lo), ('$hi', hi)]
            changed = True
        elif s.name in ['addu', 'subu', 'div']:
            # Addition/subtraction with constants
            rd, rs, rt = s
            rs_known = rs in register
            rt_known = rt in register

            if (rs_known or isinstance(rs, int)) and \
                    (rt_known or isinstance(rt, int)):
                # a = 5         ->  b = 15
                # c = 10
                # b = a + c
                rs_val = register[rs] if rs_known else rs
                rt_val = register[rt] if rt_known else rt

                if s.name == 'addu':
                    result = rs_val + rt_val
                    message = 'Constant addition: %d + %d = %d' \
                              % (rs_val, rt_val, result)

                if s.name == 'subu':
                    result = rs_val - rt_val
                    message = 'Constant subtraction: %d - %d = %d' \
                              % (rs_val, rt_val, result)

                if s.name == 'div':
                    result = rs_val / rt_val
                    message = 'Constant division: %d - %d = %d' \
                              % (rs_val, rt_val, result)

                block.replace(1, [S('command', 'li', rd, to_hex(result))],
                              message=message)
                register[rd] = result
                known.append((rd, result))
                changed = True
                continue

            if rt_known:
                # a = 10        ->  b = c + 10
                # b = c + a
                s[2] = register[rt]
                changed = True
            elif rs_known and s.name == 'addu':
                # c = 10        ->  b = a + 10
                # b = c + a
                s[1] = rt
                s[2] = register[rs]
                changed = True

            if s[2] == 0:
                # Addition/subtraction by 0
                message = '%s by 0: %s * 1' % ('Addition' if s.name == 'addu' \
                                               else 'Substraction', s[1])
                block.replace(1, [S('command', 'move', rd, s[1])], \
                              message=message)
                changed = True
        else:
            for reg in s.get_def():
                if reg in register:
                    # Known register is overwritten, remove its value
                    del register[reg]
                    known.append((reg, 'unknown'))

        if block.verbose and len(known):
            s.set_message(','.join([' %s = %s' % k for k in known]))

    return changed


#def propagate_copies(block):
#    """
#    Unpack a move instruction, by replacing its destination
#    address with its source address in the code following the move instruction.
#    This way, the move statement might be a target for dead code elimination.
#
#    move $regA, $regB           move $regA, $regB
#    ...                         ...
#    Code not writing $regA, ->  ...
#    $regB                       ...
#    ...                         ...
#    addu $regC, $regA, ...      addu $regC, $regB, ...
#    """
#    changed = False
#
#    moves = {}
#
#    block.reset()
#
#    while not block.end():
#        s = block.read()
#
#        if not s.is_command():
#            continue
#
#        if s.name == 'move':
#            # Register the move
#            reg_to, reg_from = s
#
#            if reg_from in moves:
#                if moves[reg_from] == reg_to:
#                    continue
#                else:
#                    moves[reg_to] = moves[reg_from]
#            elif reg_to == reg_from:
#                del moves[reg_to]
#            else:
#                moves[reg_to] = reg_from
#
#            s.set_message(' Move: %s = %s' % (reg_to, moves[reg_to]))
#            continue
#
#        # Replace used registers with moved equivalents when possible
#        for i, reg in s.get_use(True):
#            if reg in moves:
#                #s.replace_usage(reg, moves[reg], i)
#                #changed = True
#                replaced_before = hasattr(s, 'replaced')
#                xy = (reg, moves[reg])
#
#                if not replaced_before or xy not in s.replaced:
#                    s.replace_usage(reg, moves[reg], i)
#                    changed = True
#
#                    if replaced_before:
#                        s.replaced.append(xy)
#                    else:
#                        s.replaced = [xy]
#
#        # If a known moved register is overwritten, remove it from the
#        # registration
#        defined = s.get_def()
#        delete = []
#
#        for move_to, move_from in moves.iteritems():
#            if move_to in defined or move_from in defined:
#                delete.append(move_to)
#
#        if len(delete):
#            s.set_message(' Moves deleted: %s' % ', '.join(delete))
#
#            for reg in delete:
#                del moves[reg]
#
#    return changed


def propagate_copies(block):
    """
    Unpack a move instruction, by replacing its destination
    address with its source address in the code following the move instruction.
    This way, the move statement might be a target for dead code elimination.

    move $regA, $regB           move $regA, $regB
    ...                         ...
    Code not writing $regA, ->  ...
    $regB                       ...
    ...                         ...
    addu $regC, $regA, ...      addu $regC, $regB, ...
    """
    changed = False

    block.reset()

    while not block.end():
        s = block.read()

        # For each copy statement s: x = y do
        if s.is_command('move'):
            x, y = s

            # Moves to reserved registers will never be removed, so don't
            # bother replacing them
            if x in RESERVED_REGISTERS:
                continue

            # Determine the uses of x reached by this definition of x
            for s2 in block[block.pointer:]:
                i = s2.uses(x, True)
                replaced_before = hasattr(s2, 'replaced')

                if i != -1 and (not replaced_before \
                        or (x, y) not in s2.replaced):
                    s2.replace_usage(x, y, i)

                    if replaced_before:
                        s2.replaced.append((x, y))
                    else:
                        s2.replaced = [(x, y)]

                    changed = True

                # An assignment to x or y kills the copy statement x = y
                defined = s2.get_def()

                if x in defined or y in defined:
                    break

            # Determine uses of x in successors of the block
            # Determine if for each of those uses if this is the only
            # definition reaching it -> s in in[B_use]
            if s.sid in block.reach_out:
                for b in filter(lambda b: (x, y) in b.copy_in, succ(block)):
                    for s2 in b:
                        # Determine if for each of those uses this is the only
                        # definition reaching it -> s in in[B_use]
                        i = s2.uses(x, True)

                        if i != -1:
                            s2.replace_usage(x, y, i, block.bid)
                            changed = True

                        # An assignment to x or y kills the copy statement x =
                        # y
                        defined = s2.get_def()

                        if x in defined or y in defined:
                            break

    return changed


def eliminate_dead_code(block):
    """
    Dead code elimination:
    TODO: example...

    The algorithm used is as follows:
    - Traverse through the statements in reverse order.
    - If the statement definition is dead, remove it. A variable is dead if it
      is not used in the rest of the block, and is not in the `out' set of the
      block.
    """
    changed = False

    for n, s in enumerate(block):
        for reg in s.get_def():
            if is_reg_dead_after(reg, block, n):
                # Statement is redefined later, so this statement is useless
                if block.verbose:
                    s.stype = 'comment'
                    s.options['block'] = False
                    s.set_message(' dead register %s' % reg)
                    s.name = ' Dead:\t%s\t%s' % (s.name, ','.join(map(str, s)))
                else:
                    s.remove = True

                changed = True

    if not block.verbose:
        block.apply_filter(lambda s: not hasattr(s, 'remove'))

    return changed
