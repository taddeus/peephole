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
    - Integer variable definition is of the following form:
        li $reg, XX
        sw $reg, VAR
      save this as:
        reg[$reg] = XX
        constants[VAR] = XX
    - When a variable is used, the following happens:
        lw $reg, VAR
      save this as:
        reg[$reg] = constants[VAR]
    """
    constants = {}
    reg = {}

    while not block.end():
        s = block.read()

        if s.is_load():
            constants[s[0]] = s[1]
        elif s.is_command() and len(s) == 3:
            d, s, t = s

            if s in constants and t in constants:
                if s.name == 'addu':
                    result = s + t
                elif s.name == 'subu':
                    result = s - t
                elif s.name == 'mult':
                    result = s * t
                elif s.name == 'div':
                    result = s / t

                block.replace(1, [S('command', 'li', to_hex(result))])
                constants[d] = result
            #else:

    return False


def copy_propagation(block):
    """
    Rename values that were copied to there original, so the copy statement
    might be useless, allowing it to be removed by dead code elimination.
    """
    moves_from = []
    moves_to = []

    while not block.end():
        s = block.read()
        print "len(s)",len(s)
        if len(s) == 3:
            print "s[0] = ", s[0]
            print "s[1] = ", s[1]
            print "s[2] = ", s[2]
            
            if moves_from:
                print moves_from
                print moves_to

        if s.is_command('move') and s[0] not in moves_from:
            moves_from.append(s[0])
            moves_to.append(s[1])
            print "Added move to list."
        elif s.is_command('move'):
            for i in xrange(len(moves_to)):
                if moves_to[i] == s[0]:
                    moves_from[i] = s[1]
        elif len(s) == 3 and s[0] in moves_to:
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
                
    return False
