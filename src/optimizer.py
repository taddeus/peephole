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
