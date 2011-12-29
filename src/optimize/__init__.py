from src.dataflow import find_basic_blocks, generate_flow_graph
import src.liveness as liveness
import src.reaching_definitions as reaching_definitions

from redundancies import remove_redundant_jumps, move_1, move_2, move_3, \
        move_4, load, shift, add
from advanced import eliminate_common_subexpressions, fold_constants, \
        copy_propagation, eliminate_dead_code


def remove_redundancies(block):
    """Execute all functions that remove redundant statements."""
    callbacks = [move_1, move_2, move_3, move_4, load, shift, add]
    old_len = -1
    changed = False

    while old_len != len(block):
        old_len = len(block)

        block.reset()

        while not block.end():
            s = block.read()

            for callback in callbacks:
                if callback(s, block):
                    changed = True
                    break

    return changed


def optimize_block(block):
    """Optimize a basic block."""
    #changed = True

    #while changed:
    #    changed = False

    #    if remove_redundancies(block): changed = True
    #    if eliminate_common_subexpressions(block): changed = True
    #    if fold_constants(block): changed = True
    #    if copy_propagation(block): changed = True
    #    if eliminate_dead_code(block): changed = True
    #    print 'iteration'

    while remove_redundancies(block) \
            | eliminate_common_subexpressions(block) \
            | fold_constants(block) \
            | copy_propagation(block) \
            | eliminate_dead_code(block):
            #| algebraic_transformations(block) \
        #print 'iteration'
        pass

from copy import deepcopy
def optimize(statements, verbose=0):
    """Optimization wrapper function, calls global and basic-block level
    optimization functions."""
    # Optimize on a global level
    # TODO: only count instructions (no directives)
    statements = deepcopy(statements)
    o = len(statements)
    remove_redundant_jumps(statements)
    g = len(statements)

    # Divide into basic blocks
    blocks = find_basic_blocks(statements)

    # Perform dataflow analysis
    generate_flow_graph(blocks)
    liveness.create_in_out(blocks)
    reaching_definitions.create_in_out(blocks)

    # Optimize basic blocks
    map(optimize_block, blocks)

    # Concatenate optimized blocks to obtain
    block_statements = map(lambda b: b.statements, blocks)
    opt_blocks = reduce(lambda a, b: a + b, block_statements)
    b = len(opt_blocks)

    # Print results
    if verbose:
        print 'Original statements:            %d' % o
        print 'After global optimization:      %d (%d removed)' % (g, o - g)
        print 'After basic block optimization: %d (%d removed)' % (b, g - b)
        print 'Statements removed:             %d (%d%%)' \
                % (o - b, int((o - b) / float(b) * 100))

    return opt_blocks
