from utils import Statement as S, find_basic_blocks


def optimize_branch_jump_label(statements):
    """Optimize jumps after branches."""
    out_statements = []

    for i in xrange(len(statements)):
        if i + 3 > len(statements):
            out_statements.append(statements[i])
            continue

        stype, name, args = statements[i]
        stype2, name2, args2 = statements[i + 1]
        stype3, name3, args3 = statements[i + 2]

        if stype == 'command' and name == 'beq' and \
           stype2 == 'command' and name2 in ['j', 'jal'] and \
           stype3 == 'label' and name3 == args['args'][2]:
            out_statements.append(('command', 'bne', \
                {'args': [args['args'][0], args['args'][1], args2['args'][0]]}))
            out_statements.append(statements[1 + 2])
            i += 3
        else:
            out_statements.append(statements[i])

    return out_statements


def optimize_global(statements):
    """Optimize one-line statements in entire code."""
    old_len = -1

    while old_len != len(statements):
        old_len = len(statements)

        while not statements.end():
            s = statements.read()

            # mov $regA,$regB           ->  --- remove it
            if s.is_command() and s.name == 'move' and s[0] == s[1]:
                statements.replace(1, [])

            # mov $regA,$regB           ->  instr $regA, $regB, ...
            # instr $regA, $regA, ...
            if s.is_command() and s.name == 'move':
                ins = statements.peek()

                if ins and len(ins) >= 2 and ins[0] == s[0] and ins[1] == s[0]:
                    ins[1] = s[1]

            # instr $regA, ...          ->  instr $4, ...
            # mov $4, $regA                 jal XX
            # jal XX
            if s.is_command() and len(s):
                following = statements.peek(2)

                if len(following) == 2:
                    mov, jal = following

                    if mov.name == 'move' and mov[1] == s[0] \
                            and jal.name == 'jal':
                        s[0] = mov[0]
                        statements.replace(1, [], start=statements.pointer + 1)

            # sw $regA, XX              ->  sw $regA, XX
            # ld $regA, XX

            # shift $regA, $regA, 0     ->  --- remove it
            if s.is_shift() and s[0] == s[1] and s[2] == 0:
                statements.replace(1, [])

            # add $regA, $regA, X       ->  lw ..., X($regA)
            # lw ..., 0($regA)

            #     beq ..., $Lx          ->      bne ..., $Ly
            #     j $Ly                     $Lx:
            # $Lx:
            #if block.peek(3):
            #    block.replace(3, [nieuwe statements])

    return statements


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


def optimize(original, verbose=0):
    """optimization wrapper function, calls global and basic-block level
    optimization functions."""
    # Optimize on a global level
    opt_global = optimize_global(original)

    # Optimize basic blocks
    basic_blocks = find_basic_blocks(opt_global)
    blocks = optimize_blocks(basic_blocks)
    opt_blocks = reduce(lambda a, b: a.statements + b.statements, blocks)

    if verbose:
        o = len(original)
        g = len(opt_global)
        b = len(opt_blocks)
        print 'Original statements:             %d' % o
        print 'After global optimization:       %d' % g
        print 'After basic blocks optimization: %d' % b
        print 'Speedup:                         %d (%d%%)' \
                % (b - o, int((b - o) / o * 100))

    return opt_blocks
