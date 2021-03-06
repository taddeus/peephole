from statement import Statement as S, Block
from dataflow import find_basic_blocks, generate_flow_graph

from optimize_redundancies import remove_redundant_jumps, remove_redundancies,\
        remove_redundant_branch_jumps
from optimize_advanced import eliminate_common_subexpressions, \
        fold_constants, propagate_copies, eliminate_dead_code

import liveness
import reaching_definitions
import copy_propagation

from writer import write_statements


class Program(Block):
    def __len__(self):
        """Get the number of statements in the program."""
        return len(self.statements) if hasattr(self, 'statements') \
               else reduce(lambda a, b: len(a) + len(b), self.blocks, 0)

    def get_statements(self, add_block_comments=False):
        """Concatenate the statements of all blocks and return the resulting
        list."""
        if hasattr(self, 'statements'):
            return self.statements

        # Only add block start and end comments when in verbose mode
        if add_block_comments and self.verbose:
            get_id = lambda b: b.bid
            statements = []

            for b in self.blocks:
                message = ' Block %d (%d statements), edges from: %s' \
                          % (b.bid, len(b), map(get_id, b.edges_from))

                if hasattr(b, 'copy_in'):
                    message += ', COPY_in: %s' % list(b.copy_in)

                if hasattr(b, 'live_in'):
                    message += ', LIVE_in: %s' % list(b.live_in)

                if hasattr(b, 'reach_in'):
                    message += ', REACH_in: %s' % list(b.reach_in)

                statements.append(S('comment', message, block=False))

                statements += b.statements

                message = ' End of block %d, edges to: %s' \
                          % (b.bid, map(get_id, b.edges_to))

                if hasattr(b, 'copy_out'):
                    message += ', COPY_out: %s' % list(b.copy_out)

                if hasattr(b, 'live_out'):
                    message += ', LIVE_out: %s' % list(b.live_out)

                if hasattr(b, 'reach_out'):
                    message += ', REACH_out: %s' % list(b.reach_out)

                statements.append(S('comment', message, block=False))

            return statements

        return reduce(lambda a, b: a + b,
                      [b.statements for b in self.blocks])

    def count_instructions(self):
        """Count the number of statements that are commands or labels."""
        return len(filter(lambda s: s.is_command() or s.is_label(),
                          self.get_statements()))

    def optimize_global(self):
        """Optimize on a global level."""
        changed = False

        if not hasattr(self, 'statements'):
            self.statements = self.get_statements()

        if remove_redundant_jumps(self):
            changed = True

        if remove_redundant_branch_jumps(self):
            changed = True

        return changed

    def optimize_blocks(self):
        """Optimize on block level. Keep executing all optimizations until no
        more changes occur."""
        changed = False

        for block in self.blocks:
            if remove_redundancies(block):
                changed = True

            if eliminate_common_subexpressions(block):
                changed = True

            if fold_constants(block):
                changed = True

            if propagate_copies(block):
                changed = True

            if eliminate_dead_code(block):
                changed = True

        return changed

    def find_basic_blocks(self):
        """Divide the statement list into basic blocks."""
        self.blocks = find_basic_blocks(self.statements)

        for b in self.blocks:
            b.verbose = self.verbose

        del self.statements

    def perform_dataflow_analysis(self):
        """Perform dataflow analysis:
           - Divide the statement list into basic blocks
           - Generate flow graph
           - Create liveness sets: def, use, in, out
           - Create reaching definitions sets: gen, kill, in, out"""
        self.find_basic_blocks()
        generate_flow_graph(self.blocks)
        liveness.create_in_out(self.blocks)
        reaching_definitions.create_in_out(self.blocks)
        copy_propagation.create_in_out(self.blocks)

    def save(self, filename):
        """Save the program in the specified file."""
        f = open(filename, 'w+')
        f.write(write_statements(self.get_statements(True),
                verbose=self.verbose))
        f.close()

    def optimize(self):
        """Optimization wrapper function, calls global and basic-block level
        optimization functions."""
        # Remember original number of statements
        o = self.count_instructions()

        changed = True
        iterations = 0

        while changed:
            iterations += 1

            if self.verbose > 1:
                print 'main iteration %d', iterations

            changed = False

            # Optimize on a global level
            if self.optimize_global():
                if self.verbose > 1:
                    print 'changed on global level'

                changed = True

            # Perform dataflow analysis on new blocks
            self.perform_dataflow_analysis()

            # Optimize basic blocks
            if self.optimize_blocks():
                if self.verbose > 1:
                    print 'changed on block level'

                changed = True

        # Count number of instructions after optimization
        b = self.count_instructions()

        # Print results
        if self.verbose:
            print 'Original statements: %d' % o
            print 'Statements removed:  %d (%d%%)' \
                % (o - b, int((o - b) / float(b) * 100))
