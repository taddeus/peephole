from src.statement import Statement as S
from math import log


def reg_can_be_used_in(reg, block, start, end):
    """Check if a register addres safely be used in a block section using local
    dataflow analysis."""
    # Check if the register used or defined in the block section
    for s in block[start:end]:
        if s.uses(reg) or s.defines(reg):
            return False

    # Check if the register is used inside the block after the specified
    # section, without having been re-assigned first
    for s in block[end:]:
        if s.uses(reg):
            return False
        elif s.defines(reg):
            return True

    return True


def find_free_reg(block, start, end):
    """Find a temporary register that is free in a given list of statements."""
    for i in xrange(8, 16):
        tmp = '$%d' % i

        if reg_can_be_used_in(tmp, block, start, end):
            return tmp

    raise Exception('No temporary register is available.')


def eliminate_common_subexpressions(block):
    """
    Common subexpression elimination:
    x = a + b           ->  u = a + b
    y = a + b               x = u
                            y = u

    The algorithm used is as follows:
    - Traverse through the statements in reverse order.
    - If the statement can be possibly be eliminated, walk further collecting
      all other occurrences of the expression until one of the arguments is
      assigned in a statement, or the start of the block has been reached.
    - If one or more occurrences were changed, insert the expression with a new
      destination address before the last changed occurrence and change all
      occurrences to a move instruction from that address.
    """
    changed = False

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
                new_reg = find_free_reg(block, occurrences[0], occurrences[-1])

                # Replace all occurrences with a move statement
                for occurrence in occurrences:
                    rd = block[occurrence][0]
                    block.replace(1, [S('command', 'move', rd, new_reg)], \
                            start=occurrence)

                # Insert the calculation before the original with the new
                # destination address
                block.insert(S('command', s.name, *([new_reg] + args)), \
                             index=occurrences[0])

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

    while not block.end():
        s = block.read()

        if not s.is_command():
            continue

        if s.name == 'li':
            # Save value in register
            register[s[0]] = int(s[1], 16)
        elif s.name == 'move' and s[0] in register:
            reg_to, reg_from = s

            if reg_from in register:
                # Other value is also known, copy its value
                register[reg_to] = register[reg_to]
            else:
                # Other value is unknown, delete the value
                del register[reg_to]
        elif s.name == 'sw' and s[0] in register:
            # Constant variable definition, e.g. 'int a = 1;'
            constants[s[1]] = register[s[0]]
        elif s.name == 'lw' and s[1] in constants:
            # Usage of variable with constant value
            register[s[0]] = constants[s[1]]
        elif s.name in ['addu', 'subu', 'mult', 'div']:
            # Calculation with constants
            rd, rs, rt = s[0], s[1], s[2]
            rs_known = rs in register
            rt_known = rt in register

            if rs_known and rt_known:
                # a = 5         ->  b = 15
                # c = 10
                # b = a + c
                rs_val = register[rs]
                rt_val = register[rt]

                if s.name == 'addu':
                    result = to_hex(rs_val + rt_val)

                if s.name == 'subu':
                    result = to_hex(rs_val - rt_val)

                if s.name == 'mult':
                    result = to_hex(rs_val * rt_val)

                if s.name == 'div':
                    result = to_hex(rs_val / rt_val)

                block.replace(1, [S('command', 'li', rd, result)])
                register[rd] = result
                changed = True
            elif rt_known:
                # c = 10        ->  b = a + 10
                # b = c + a
                s[2] = register[rt]
                changed = True
            elif rs_known and s.name == 'addu':
                # a = 10        ->  b = c + 10
                # b = c + a
                s[1] = rt
                s[2] = register[rs]
                changed = True
        elif len(s) and s[0] in register:
            # Known register is overwritten, remove its value
            del register[s[0]]

    return changed


def copy_propagation(block):
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
    moves_from = []
    moves_to = []
    changed = False

    while not block.end():
        s = block.read()

        if s.is_command('move') and s[0] not in moves_to:
            # Add this move to the lists, because it is not yet there.
            moves_from.append(s[1])
            moves_to.append(s[0])
        elif s.is_command('move') and s[0] in moves_to:
            # This move is already in the lists, so only update it
            for i in xrange(len(moves_to)):
                if moves_to[i] == s[0]:
                    moves_from[i] = s[1]
                    break
        elif (len(s) == 3 or s.is_command('mlfo') or s.is_load()) \
                and (s[0] in moves_to or s[0] in moves_from):
            # One of the registers gets overwritten, so remove the data from
            # the list.
            i = 0
            while i  < len(moves_to):
                if moves_to[i] == s[0] or moves_to[i] == s[1]:
                    del moves_to[i]
                    del moves_from[i]
                else:
                    i += 1
        elif len(s) == 3 and (s[1] in moves_to or s[2] in moves_to):
            # Check where the result of the move is used and replace it with
            # the original variable.
            for i in xrange(len(moves_to)):
                if s[1] == moves_to[i]:
                    s[1] = moves_from[i]
                    break

                if s[2] == moves_to[i]:
                    s[2] = moves_from[i]
                    break

            changed = True

    return changed


def algebraic_transformations(block):
    """
    Change ineffective or useless algebraic expressions. Handled are:
    - x = y + 0 -> x = y
    - x = y - 0 -> x = y
    - x = y * 1 -> x = y
    - x = y * 0 -> x = 0
    - x = y * 2 -> x = x << 1
    """
    changed = False

    while not block.end():
        s = block.read()

        if (s.is_command('addu') or s.is_command('subu')) and s[2] == 0:
            block.replace(1, [S('command', 'move', s[0], s[1])])
            changed = True
        elif s.is_command('mult'):
            next = block.peek()
            if next.is_command('mflo'):
                if s[1] == 1:
                    block.replace(2, [S('command', 'move', next[0], s[0])])
                    changed = True
                    break
                elif s[1] == 0:
                    block.replace(2, [S('command', 'li', '$1', to_hex(0))])
                    changed = True
                    break

                shift_amount = log(s[1], 2)
                if shift_amount.is_integer():
                    new_command = S('command', 'sll', next[0], s[0], int(shift_amount))
                    block.replace(2, [new_command])
                    changed = True

    return changed
