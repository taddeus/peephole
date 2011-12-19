def equal_mov(s):
    '''Check for useless move operations.'''
    return s.is_command() and s.name == 'move' and s[0] == s[1]

def empty_shift(s):
    '''Check for useless shift operations.'''
    return s.is_shift() and s[0] == s[1] and s[2] == 0

def optimize_branch_jump_label(statements):
    '''Optimize jumps after branches.'''
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
    '''Optimize one-line statements in entire code.'''
    statements = optimize_branch_jump_label(statements)

    return filter(lambda s: not equal_mov(s) and not empty_shift(s), statements)

def optimize_blocks(blocks):
    '''Call the optimizer for each basic block. Do this several times until
    no more optimizations are achieved.'''
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
    '''Optimize a basic block.'''
    changed = False
    output_statements = []

    for statement in statements:
        new_statement = statement

        output_statements.append(new_statement)

    return changed, output_statements
