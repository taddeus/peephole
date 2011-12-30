from src.dataflow import find_basic_blocks, generate_flow_graph
from redundancies import remove_redundancies
from advanced import eliminate_common_subexpressions, fold_constants, \
        copy_propagation, eliminate_dead_code
import src.liveness as liveness
import src.reaching_definitions as reaching_definitions

def optimize(program, verbose=0):
    """Optimization wrapper function, calls global and basic-block level
    optimization functions."""
    # Remember original number of statements
    o = program.count_instructions()

    changed = True

    while changed:
        changed = False

        # Optimize on a global level
        if program.optimize_global():
            changed = True

        # Perform dataflow analysis on new blocks
        program.perform_dataflow_analysis()

        # Optimize basic blocks
        if program.optimize_blocks():
            changed = True

    # Count number of instructions after optimization
    b = program.count_instructions()

    # Print results
    if verbose:
        print 'Original statements:            %d' % o
        print 'Statements removed:             %d (%d%%)' \
                % (o - b, int((o - b) / float(b) * 100))
