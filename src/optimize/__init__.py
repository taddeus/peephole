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

    # Optimize on a global level
    program.optimize_global()
    g = program.count_instructions()

    # Perform dataflow analysis
    program.perform_dataflow_analysis()

    # Optimize basic blocks
    program.optimize_blocks()

    # Concatenate optimized blocks to obtain
    b = program.count_instructions()

    # Print results
    if verbose:
        print 'Original statements:            %d' % o
        print 'After global optimization:      %d (%d removed)' % (g, o - g)
        print 'After basic block optimization: %d (%d removed)' % (b, g - b)
        print 'Statements removed:             %d (%d%%)' \
                % (o - b, int((o - b) / float(b) * 100))
