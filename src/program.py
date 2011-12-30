from statement import Statement as S, Block
from dataflow import find_basic_blocks, generate_flow_graph
from optimize.redundancies import remove_redundant_jumps, remove_redundancies
from optimize.advanced import eliminate_common_subexpressions, \
        fold_constants, copy_propagation, eliminate_dead_code
from writer import write_statements
import liveness
import reaching_definitions


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

        # Only add block start and end comments when in debug mode
        if add_block_comments and self.debug:
            get_id = lambda b: b.bid
            statements = []

            for b in self.blocks:
                message = ' Block %d (%d statements), edges from: %s' \
                          % (b.bid, len(b), map(get_id, b.edges_from))

                if hasattr(b, 'live_in'):
                    message += ', LIVE_in: %s' % list(b.live_in)

                if hasattr(b, 'reach_in'):
                    message += ', REACH_in: %s' % list(b.reach_in)

                statements.append(S('comment', message, block=False))

                statements += b.statements

                message = ' End of block %d, edges to: %s' \
                          % (b.bid, map(get_id, b.edges_to))

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
        if not hasattr(self, 'statements'):
            self.statements = self.get_statements()

        return remove_redundant_jumps(self)

    def optimize_blocks(self):
        """Optimize on block level. Keep executing all optimizations until no
        more changes occur."""
        self.program_iterations = self.block_iterations = 0
        program_changed = True

        while program_changed:
            self.program_iterations += 1
            program_changed = False

            for block in self.blocks:
                self.block_iterations += 1
                block_changed = True

                while block_changed:
                    block_changed = False

                    if remove_redundancies(block):
                        block_changed = True

                    if eliminate_common_subexpressions(block):
                        block_changed = True

                    if fold_constants(block):
                        block_changed = True

                    if copy_propagation(block):
                        block_changed = True

                    if eliminate_dead_code(block):
                        block_changed = True

                    if block_changed:
                        program_changed = True

    def find_basic_blocks(self):
        """Divide the statement list into basic blocks."""
        self.blocks = find_basic_blocks(self.statements)

        for b in self.blocks:
            b.debug = self.debug

        # Remove the old statement list, since it will probably change
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

    def save(self, filename):
        """Save the program in the specified file."""
        f = open(filename, 'w+')
        f.write(write_statements(self.get_statements(True)))
        f.close()
