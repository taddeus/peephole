from src.statement import Statement as S


def create_variable():
    return '$15'


def eliminate_common_subexpressions(block):
    """
    Common subexpression elimination:
    - Traverse through the statements in reverse order.
    - If the statement can be possibly be eliminated, walk further collecting
      all other occurrences of the expression until one of the arguments is
      assigned in a statement, or the start of the block has been reached.
    - If one or more occurrences were found, insert the expression with a new
      destination address before the last found occurrence and change all
      occurrences to a move instruction from that address.
    """
    found = False
    block.reverse_statements()

    while not block.end():
        s = block.read()

        if s.is_arith():
            pointer = block.pointer
            last = False
            new_reg = False
            args = s[1:]

            # Collect similar statements
            while not block.end():
                s2 = block.read()

                # Stop if one of the arguments is assigned
                if len(s2) and s2[0] in args:
                    break

                # Replace a similar expression by a move instruction
                if s2.name == s.name and s2[1:] == args:
                    if not new_reg:
                        new_reg = create_variable()

                    block.replace(1, [S('command', 'move', s2[0], new_reg)])
                    last = block.pointer

            # Insert an additional expression with a new destination address
            if last:
                block.insert(S('command', s.name, [new_reg] + args), last)
                found = True

            # Reset pointer to and continue from the original statement
            block.pointer = pointer

    block.reverse_statements()

    return found


def to_hex(value):
    """Create the hexadecimal string of an integer."""
    return '0x%08x' % value


def fold_constants(block):
    """
    Constant folding:
    - An immidiate load defines a register value:
        li $reg, XX     ->  register[$reg] = XX
    - Integer variable definition is of the following form:
        li $reg, XX     ->  constants[VAR] = XX
        sw $reg, VAR    ->  register[$reg] = XX
    - When a variable is used, the following happens:
        lw $reg, VAR    ->  register[$reg] = constants[VAR]
    """
    found = False

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
            rd, rs, rt = s
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

                block.replace(1, [S('command', 'li', result)])
                register[rd] = result
                found = True
            elif rt_known:
                # c = 10        ->  b = a + 10
                # b = c + a
                s[2] = register[rt]
                found = True
            elif rs_known and s.name in ['addu', 'mult']:
                # a = 10        ->  b = c + 10
                # b = c + a
                s[1] = rt
                s[2] = register[rs]
                found = True
        elif len(s) and s[0] in register:
            # Known register is overwritten, remove its value
            del register[s[0]]

    return found


def copy_propagation(block):
    """
    Rename values that were copied to there original, so the copy statement
    might be useless, allowing it to be removed by dead code elimination.
    """
    moves_from = []
    moves_to = []

    while not block.end():
        s = block.read()
        
        if len(s) == 3:
            print "s[0] = ", s[0]
            print "s[1] = ", s[1]
            print "s[2] = ", s[2]
            
            if moves_from:
                print "fr: ", moves_from
                print "to: ", moves_to

        if s.is_command('move') and s[0] not in moves_to:
            moves_from.append(s[1])
            moves_to.append(s[0])
            print "Added move to list."
        elif s.is_command('move'):
            for i in xrange(len(moves_to)):
                if moves_to[i] == s[0]:
                    moves_from[i] = s[1]
        elif len(s) == 3 and s[0] in moves_to:
            print len(s)
            print len(moves_to)
            for i in xrange(len(moves_to)):
                if moves_to[i] == s[0]:
                    del moves_to[i]
                    del moves_from[i]
                    "Removed move from list."
        elif len(s) == 3 and (s[1] in moves_to or s[2] in moves_to):
            print "Have to propagate."
            for i in xrange(len(moves_to)):
                if s[1] == moves_to[i]:
                    s[1] = moves_from[i]
                    print "Propagated"
                
                if s[2] == moves_to[i]:
                    s[2] = moves_from[i]
                    print "Propagated"
                    
        print ""       
    return False
