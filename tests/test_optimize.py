import unittest

from src.optimize.redundancies import remove_redundancies, remove_redundant_jumps
from src.program import Program
from src.statement import Statement as S, Block as B


def optimize_block(block):
    """Optimize a basic block using a Program object."""
#    program = Program([])

#    program.blocks = [block]
#    del program.statements
    
#   program.optimize_blocks()

    remove_redundancies(block)
    eliminate_common_subexpressions(block)
    fold_constants(block)
    copy_propagation(block)

    return program.blocks


class TestOptimize(unittest.TestCase):

    def setUp(self):
        self.foo = S('command', 'foo')
        self.bar = S('command', 'bar')

    def tearDown(self):
        del self.foo
        del self.bar

    def test_optimize_block_movaa(self):
        block = B([self.foo,
                   S('command', 'move', '$regA', '$regA'),
                   self.bar])
        remove_redundancies(block)
        self.assertEquals(block.statements, [self.foo, self.bar])

    def test_optimize_block_movab(self):
        move = S('command', 'move', '$regA', '$regB')
        block = B([self.foo,
                   move,
                   self.bar])
        remove_redundancies(block)
        self.assertEquals(block.statements, [self.foo, move, self.bar])

    def test_optimize_block_movinst_true(self):
        block = B([self.foo,
                   S('command', 'move', '$regA', '$regB'),
                   S('command', 'addu', '$regA', '$regA', 2),
                   self.bar])
        remove_redundancies(block)
        self.assertEquals(block.statements, [self.foo,
                   S('command', 'addu', '$regA', '$regB', 2),
                   self.bar])

    def test_optimize_block_movinst_false(self):
        statements = [self.foo, \
                      S('command', 'move', '$regA', '$regB'), \
                      S('command', 'addu', '$regD', '$regC', 2), \
                      self.bar]

        block = B(statements)
        remove_redundancies(block)
        self.assertEquals(block.statements, statements)

    def test_optimize_block_instr_mov_jal_true(self):
        block = B([self.foo,
                   S('command', 'addu', '$regA', '$regC', 2),
                   S('command', 'move', '$4', '$regA'),
                   S('command', 'jal', 'L1'),
                   self.bar])
        remove_redundancies(block)

        self.assertEquals(block.statements, [self.foo,
                   S('command', 'addu', '$4', '$regC', 2),
                   S('command', 'jal', 'L1'),
                   self.bar])

    def test_optimize_block_instr_mov_jal_false(self):
        arguments = [self.foo, \
                     S('command', 'addu', '$regA', '$regC', 2), \
                     S('command', 'move', '$3', '$regA'), \
                     S('command', 'jal', 'L1'), \
                     self.bar]
        block = B(arguments)
        remove_redundancies(block)

        self.assertEquals(block.statements, arguments)

    def test_optimize_block_sw_ld_true(self):
        block = B([self.foo,
                   S('command', 'sw', '$regA', '$regB'),
                   S('command', 'lw', '$regA', '$regB'),
                   self.bar])
        remove_redundancies(block)

        self.assertEquals(block.statements, [self.foo,
                   S('command', 'sw', '$regA', '$regB'),
                   self.bar])

    def test_optimize_block_sw_ld_false(self):
        arguments = [self.foo, \
                     S('command', 'sw', '$regA', '$regB'), \
                     S('command', 'lw', '$regD', '$regC'), \
                     self.bar]
        block = B(arguments)
        remove_redundancies(block)

        self.assertEquals(block.statements, arguments)

    def test_optimize_block_shift_true(self):
        block = B([self.foo,
                   S('command', 'sll', '$regA', '$regA', 0),
                   self.bar])
        remove_redundancies(block)

        self.assertEquals(block.statements, [self.foo, self.bar])

    def test_optimize_block_shift_false(self):
        arguments = [self.foo, \
                     S('command', 'sll', '$regA', '$regB', 0), \
                     self.bar]
        block = B(arguments)
        remove_redundancies(block)

        self.assertEquals(block.statements, arguments)

        arguments2 = [self.foo, \
                     S('command', 'sll', '$regA', '$regA', 1), \
                     self.bar]
        block2 = B(arguments2)
        remove_redundancies(block2)

        self.assertEquals(block2.statements, arguments2)

    def test_optimize_block_add_lw_true(self):
        block = B([self.foo,
                   S('command', 'addu', '$regA', '$regA', 10),
                   S('command', 'lw', '$regB', '0($regA)'),
                   self.bar])
        remove_redundancies(block)

        self.assertEquals(block.statements, [self.foo,
                   S('command', 'lw', '$regB', '10($regA)'),
                   self.bar])

    def test_optimize_block_add_lw_false(self):
        arguments = [self.foo, \
                     S('command', 'addu', '$regA', '$regA', 10), \
                     S('command', 'lw', '$regB', '0($regC)'), \
                     self.bar]
        block = B(arguments)
        remove_redundancies(block)

        arguments2 = [self.foo, \
                     S('command', 'addu', '$regA', '$regB', 10), \
                     S('command', 'lw', '$regB', '0($regA)'), \
                     self.bar]
        block2 = B(arguments2)

        arguments3 = [self.foo, \
                     S('command', 'addu', '$regA', '$regA', 10), \
                     S('command', 'lw', '$regB', '1($regA)'), \
                     self.bar]
        block3 = B(arguments3)
        remove_redundancies(block3)

        self.assertEquals(block.statements, arguments)
        self.assertEquals(block2.statements, arguments2)
        self.assertEquals(block3.statements, arguments3)
        
    def test_optimize_block_move_move_true(self):
        block = B([self.foo,
                   S('command', 'move', '$regA', '$regB'),
                   S('command', 'move', '$regB', '$regA'),
                   self.bar])
        remove_redundancies(block)

        self.assertEquals(block.statements, [self.foo,
                   S('command', 'move', '$regA', '$regB'),
                   self.bar])

    def test_optimize_block_mov_mov_false(self):
        arguments = [self.foo, \
                     S('command', 'move', '$regA', '$regB'), \
                     S('command', 'move', '$regB', '$regC'), \
                     self.bar]
        block = B(arguments)
        remove_redundancies(block)

        self.assertEquals(block.statements, arguments)
        
    def test_remove_redundant_jumps_true(self):
        block = B([self.foo,
                   S('command', 'j', '$L1'),
                   S('label', '$L1'),
                   self.bar])
                   
       remove_redundancies(block)
       
       self.assertEqual(block.statements, B([self.foo, 
                                             S('command', 'j', '$L1'),
                                             self.bar]))
                                             
    def test_remove_redundant_jumps_false(self):
        arguments = [self.foo,
                   S('command', 'j', '$L1'),
                   S('label', '$L2'),
                   self.bar]
        block = B(arguments)
                   
       remove_redundancies(block)
       
       self.assertEqual(block.statements, arguments)
        
    def test_remove_redundant_branch_jumps_beq_j_true(self):
        block = B([self.foo,
                   S('command', 'beq', '$regA', '$regB', '$Lx'),
                   S('command', 'j', '$Ly'),
                   S('label', '$Lx'),
                   self.bar])
        remove_redundant_branch_jumps(block)

        self.assertEquals(block.statements, [self.foo,
                   S('command', 'bne', '$regA', '$regB', '$Ly'),
                   S('label', '$Lx'),
                   self.bar])

    def test_remove_redundant_branch_jumps_beq_j_false(self):
        arguments = [self.foo, \
                     S('command', 'beq', '$regA', '$regB', '$Lz'), \
                     S('command', 'j', '$Ly'), \
                     S('label', '$Lx'), \
                     self.bar]
        block = B(arguments)
        remove_redundant_branch_jumps(block)

        self.assertEquals(block.statements, arguments)

    def test_remove_redundant_branch_jumps_bne_j_true(self):
        block = B([self.foo,
                   S('command', 'bne', '$regA', '$regB', '$Lx'),
                   S('command', 'j', '$Ly'),
                   S('label', '$Lx'),
                   self.bar])
        remove_redundant_branch_jumps(block)

        self.assertEquals(block.statements, [self.foo,
                   S('command', 'beq', '$regA', '$regB', '$Ly'),
                   S('label', '$Lx'),
                   self.bar])

    def test_remove_redundant_branch_jumps_bne_j_false(self):
        arguments = [self.foo, \
                     S('command', 'bne', '$regA', '$regB', '$Lz'), \
                     S('command', 'j', '$Ly'), \
                     S('label', '$Lx'), \
                     self.bar]
        block = B(arguments)
        remove_redundant_branch_jumps(block)

        self.assertEquals(block.statements, arguments)
