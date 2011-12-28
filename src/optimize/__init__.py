from src.dataflow import find_basic_blocks

from standard import redundant_move_1, redundant_move_2, \
        redundant_move_3, redundant_move_4, redundant_load, \
        redundant_shift, redundant_add
from advanced import eliminate_common_subexpressions, fold_constants, \
    copy_propagation


def optimize_global(statements):
    """Optimize statement sequences on a global level."""
    old_len = -1

    while old_len != len(statements):
        old_len = len(statements)

        while not statements.end():
            s = statements.read()

            #     beq/bne ..., $Lx      ->      bne/beq ..., $Ly
            #     j $Ly                     $Lx:
            # $Lx:
            if s.is_command('beq', 'bne'):
                following = statements.peek(2)

                if len(following) == 2:
                    j, label = following

                    if j.is_command('j') and label.is_label(s[2]):
                        s.name = 'bne' if s.is_command('beq') else 'beq'
                        s[2] = j[0]
                        statements.replace(3, [s, label])


def optimize_block(block):
    """Optimize a basic block."""
    standard = [redundant_move_1, redundant_move_2, redundant_move_3, \
                redundant_move_4, redundant_load, redundant_shift, \
                redundant_add]
    old_len = -1

    # Standard optimizations
    while old_len != len(block):
        old_len = len(block)

        while not block.end():
            s = block.read()

            for callback in standard:
                if callback(s, block):
                    break

    # Advanced optimizations
    #changed = True

    #while changed:
    #    changed = eliminate_common_subexpressions(block) \
    #              or fold_constants(block)

    while eliminate_common_subexpressions(block) \
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
