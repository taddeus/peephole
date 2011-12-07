def equal_mov(statement):
    '''Check for useless move operations.'''
    stype, name, args = statement
    return stype == 'command' and name == 'move' \
        and args['args'][0] == args['args'][1]
    
def empty_shift(statement):
    '''Check for useless shift operations.'''
    shift_types = ['sll', 'sla', 'srl', 'sra']
    stype, name, args = statement
    return stype == 'command' and name in shift_types and \
        args['args'][0] == args['args'][1] and args['args'][2] == 0

def optimize_global(statements):
    '''Optimize one-line statements in entire code.'''
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
