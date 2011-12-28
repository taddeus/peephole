from src.dataflow import find_basic_blocks

from redundancies import remove_redundant_jumps, move_1, move_2, move_3, \
        move_4, load, shift, add
from advanced import eliminate_common_subexpressions, fold_constants, \
        copy_propagation


def remove_redundancies(block):
    """Execute all functions that remove redundant statements."""
    callbacks = [move_1, move_2, move_3, move_4, load, shift, add]
    old_len = -1
    changed = False

    while old_len != len(block):
        old_len = len(block)

        while not block.end():
            s = block.read()

            for callback in callbacks:
                if callback(s, block):
                    changed = True
                    break

    return changed


def optimize_block(block):
    """Optimize a basic block."""
    while remove_redundancies(block) \
            | eliminate_common_subexpressions(block) \
            | fold_constants(block) \
            | copy_propagation(block):
        pass

def optimize(statements, verbose=0):
    """Optimization wrapper function, calls global and basic-block level
    optimization functions."""
    # Optimize on a global level
    o = len(statements)
    optimize_global(statements)
    g = len(statements)

    # Optimize basic blocks
    blocks = find_basic_blocks(statements)
    map(optimize_block, blocks)
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
        print 'Optimization:                    %d (%d%%)' \
                % (b - o, int((b - o) / float(o) * 100))

    return opt_blocks
