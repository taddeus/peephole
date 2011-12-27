import re

from dataflow import find_basic_blocks


def optimize_global(statements):
    """Optimize statement sequences on a global level."""
    old_len = -1

    while old_len != len(statements):
        old_len = len(statements)

        while not statements.end():
            s = statements.read()

            # mov $regA, $regA          ->  --- remove it
            if s.is_command('move') and s[0] == s[1]:
                statements.replace(1, [])
                continue

            # mov $regA, $regB          ->  instr $regA, $regB, ...
            # instr $regA, $regA, ...
            if s.is_command('move'):
                ins = statements.peek()

                if ins and len(ins) >= 2 and ins[0] == s[0] and ins[1] == s[0]:
                    ins[1] = s[1]
                    statements.replace(2, [ins])
                    continue

            # instr $regA, ...          ->  instr $4, ...
            # mov $4, $regA                 jal XX
            # jal XX
            if s.is_command() and len(s):
                following = statements.peek(2)

                if len(following) == 2:
                    mov, jal = following

                    if mov.is_command('move') and mov[1] == s[0] \
                            and re.match('^\$[4-7]$', mov[0]) \
                            and jal.is_command('jal'):
                        s[0] = mov[0]
                        statements.replace(2, [s])
                        continue

            # sw $regA, XX              ->  sw $regA, XX
            # ld $regA, XX
            if s.is_command('sw'):
                ld = statements.peek()

                if ld.is_command('ld') and ld[0] == s[0]:
                    statements.replace(2, [s])
                    continue

            # shift $regA, $regA, 0     ->  --- remove it
            if s.is_shift() and s[0] == s[1] and s[2] == 0:
                statements.replace(1, [])
                continue

            # add $regA, $regA, X       ->  lw ..., X($regA)
            # lw ..., 0($regA)
            if s.is_command('add') and s[0] == s[1]:
                lw = statements.peek()

                if lw.is_command('lw') and lw[-1] == '0(%s)' % s[0]:
                    lw[-1] = str(s[2]) + lw[-1][1:]
                    statements.replace(2, [lw])
                    continue

            #     beq ..., $Lx          ->      bne ..., $Ly
            #     j $Ly                     $Lx:
            # $Lx:
            if s.is_command('beq'):
                following = statements.peek(2)

                if len(following) == 2:
                    j, label = following

                    if j.is_command('j') and label.is_label(s[2]):
                        s.name = 'bne'
                        s[2] = j[0]
                        statements.replace(3, [s, label])
                        
            #     bne ..., $Lx          ->      beq ..., $Ly
            #     j $Ly                     $Lx:
            # $Lx:
            if s.is_command('bne'):
                following = statements.peek(2)

                if len(following) == 2:
                    j, label = following

                    if j.is_command('j') and label.is_label(s[2]):
                        s.name = 'beq'
                        s[2] = j[0]
                        statements.replace(3, [s, label])


def optimize_blocks(blocks):
    """Call the optimizer for each basic block. Do this several times until
    no more optimizations are achieved."""
    changed = True

    while changed:
        changed = False
        optimized = []

        for block in blocks:
            block_changed, b = optimize_block(block)
            optimized.append(b)

            if block_changed:
                changed = True

        blocks = optimized

    return reduce(lambda a, b: a + b, blocks, [])


def optimize_block(statements):
    """Optimize a basic block."""
    changed = False
    output_statements = []

    for statement in statements:
        new_statement = statement

        output_statements.append(new_statement)

    return changed, output_statements


def optimize(statements, verbose=0):
    """optimization wrapper function, calls global and basic-block level
    optimization functions."""
    # Optimize on a global level
    o = len(statements)
    optimize_global(statements)
    g = len(statements)

    # Optimize basic blocks
    basic_blocks = find_basic_blocks(statements)
#    blocks = optimize_blocks(basic_blocks)
    blocks = basic_blocks
    block_statements = map(lambda b: b.statements, blocks)
    opt_blocks = reduce(lambda a, b: a + b, block_statements)
    b = len(opt_blocks)

    # - Common subexpression elimination
    # - Constant folding
    # - Copy propagation
    # - Dead-code elimination
    # - Temporary variable renaming
    # - Interchange of independent statements

    if verbose:
        print 'Original statements:             %d' % o
        print 'After global optimization:       %d' % g
        print 'After basic blocks optimization: %d' % b
        print 'Speedup:                         %d (%d%%)' \
                % (b - o, int((b - o) / o * 100))

    return opt_blocks
