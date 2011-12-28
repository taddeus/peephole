import unittest

from src.optimize import optimize_global, optimize_block, optimize_blocks
from src.statement import Statement as S, Block as B


class TestOptimize(unittest.TestCase):

    def setUp(self):
        pass

    def test_optimize_block_movaa(self):
        foo = S('command', 'foo')
        bar = S('command', 'bar')
        block = B([foo,
                   S('command', 'move', '$regA', '$regA'),
                   bar])
        optimize_block(block)
        self.assertEquals(block.statements, [foo, bar])
        
    def test_optimize_block_movab(self):
        foo = S('command', 'foo')
        move = S('command', 'move', '$regA', '$regB')
        bar = S('command', 'bar')
        block = B([foo,
                   move,
                   bar])
        optimize_block(block)
        self.assertEquals(block.statements, [foo, move, bar])
        
    def test_optimize_block_movinst_true(self):
        foo = S('command', 'foo')
        bar = S('command', 'bar')
        
        block = B([foo,
                   S('command', 'move', '$regA', '$regB'),
                   S('command', 'addu', '$regA', '$regA', 2),
                   bar])
        optimize_block(block)
        self.assertEquals(block.statements, [foo,                     
                   S('command', 'addu', '$regA', '$regB', 2),      
                   bar])
                   
    def test_optimize_block_movinst_false(self):
        foo = S('command', 'foo')
        bar = S('command', 'bar')
        statements = [foo, \
                      S('command', 'move', '$regA', '$regB'), \
                      S('command', 'addu', '$regA', '$regC', 2), \
                      bar]
        
        block = B(statements)
        optimize_block(block)
        self.assertEquals(block.statements, statements)
                
    def test_optimize_block_instr_mov_jal_true(self):
        foo = S('command', 'foo')
        bar = S('command', 'bar')
        
        block = B([foo,
                   S('command', 'addu', '$regA', '$regC', 2),
                   S('command', 'move', '$4', '$regA'),
                   S('command', 'jal', 'L1'),
                   bar])
        optimize_block(block)
        
        self.assertEquals(block.statements, [foo,                     
                   S('command', 'addu', '$4', '$regC', 2),
                   S('command', 'jal', 'L1'),      
                   bar])
        
    def test_optimize_block_instr_mov_jal_false(self):
        foo = S('command', 'foo')
        bar = S('command', 'bar')
        
        arguments = [foo, \
                      S('command', 'addu', '$regA', '$regC', 2), \
                      S('command', 'move', '$3', '$regA'), \
                      S('command', 'jal', 'L1'), \
                      bar]
        block = B(arguments)
        optimize_block(block)
        
        self.assertEquals(block.statements, arguments)
        
    def test_optimize_block_sw_ld_true(self):
        foo = S('command', 'foo')
        bar = S('command', 'bar')
        
        block = B([foo,
                   S('command', 'sw', '$regA', '$regB'),
                   S('command', 'ld', '$regA', '$regC'),
                   bar])
        optimize_block(block)
        
        self.assertEquals(block.statements, [foo,
                   S('command', 'sw', '$regA', '$regB'),
                   bar])
                   
    def test_optimize_block_sw_ld_false(self):
        foo = S('command', 'foo')
        bar = S('command', 'bar')
        
        arguments = [foo, \
                     S('command', 'sw', '$regA', '$regB'), \
                     S('command', 'ld', '$regD', '$regC'), \
                     bar]
        block = B(arguments)
        optimize_block(block)
        
        self.assertEquals(block.statements, arguments)

    def test_optimize_block_shift_true(self):
        foo = S('command', 'foo')
        bar = S('command', 'bar')
        
        block = B([foo,
                   S('command', 'sll', '$regA', '$regA', 0),
                   bar])
        optimize_block(block)
        
        self.assertEquals(block.statements, [foo,
                   bar])
                   
    def test_optimize_block_shift_false(self):
        foo = S('command', 'foo')
        bar = S('command', 'bar')
        
        arguments = [foo, \
                     S('command', 'sll', '$regA', '$regB', 0), \
                     bar]
        block = B(arguments)
        optimize_block(block)
        
        self.assertEquals(block.statements, arguments)
        
        arguments2 = [foo, \
                     S('command', 'sll', '$regA', '$regA', 1), \
                     bar]
        block2 = B(arguments2)
        optimize_block(block2)
        
        self.assertEquals(block2.statements, arguments2)
    
    def test_optimize_block_add_lw_true(self):
        foo = S('command', 'foo')
        bar = S('command', 'bar')
        
        block = B([foo,
                   S('command', 'add', '$regA', '$regA', 10),
                   S('command', 'lw', '$regB', '0($regA)'),
                   bar])
        optimize_block(block)
        
        self.assertEquals(block.statements, [foo,
                   S('command', 'lw', '$regB', '10($regA)'),
                   bar])
                   
    def test_optimize_block_add_lw_false(self):
        foo = S('command', 'foo')
        bar = S('command', 'bar')
        
        arguments = [foo, \
                     S('command', 'add', '$regA', '$regA', 10), \
                     S('command', 'lw', '$regB', '0($regC)'), \
                     bar]
        block = B(arguments)
        optimize_block(block)
        
        arguments2 = [foo, \
                     S('command', 'add', '$regA', '$regB', 10), \
                     S('command', 'lw', '$regB', '0($regA)'), \
                     bar]
        block2 = B(arguments2)
        
        arguments3 = [foo, \
                     S('command', 'add', '$regA', '$regA', 10), \
                     S('command', 'lw', '$regB', '1($regA)'), \
                     bar]
        block3 = B(arguments3)
        optimize_block(block3)
        
        self.assertEquals(block.statements, arguments)
        self.assertEquals(block2.statements, arguments2)
        self.assertEquals(block3.statements, arguments3)
        
    def test_optimize_global_beq_j_true(self):
        foo = S('command', 'foo')
        bar = S('command', 'bar')
        
        block = B([foo,
                   S('command', 'beq', '$regA', '$regB', '$Lx'),
                   S('command', 'j', '$Ly'),
                   S('label', '$Lx'),
                   bar])
        optimize_global(block)
        
        self.assertEquals(block.statements, [foo,
                   S('command', 'bne', '$regA', '$regB', '$Ly'),
                   S('label', '$Lx'),
                   bar])
                   
    def test_optimize_global_beq_j_false(self):
        foo = S('command', 'foo')
        bar = S('command', 'bar')
        
        arguments = [foo, \
                     S('command', 'beq', '$regA', '$regB', '$Lz'), \
                     S('command', 'j', '$Ly'), \
                     S('label', '$Lx'), \
                     bar]
        block = B(arguments)
        optimize_global(block)
        
        self.assertEquals(block.statements, arguments)
        
    def test_optimize_global_bne_j_true(self):
        foo = S('command', 'foo')
        bar = S('command', 'bar')
        
        block = B([foo,
                   S('command', 'bne', '$regA', '$regB', '$Lx'),
                   S('command', 'j', '$Ly'),
                   S('label', '$Lx'),
                   bar])
        optimize_global(block)
        
        self.assertEquals(block.statements, [foo,
                   S('command', 'beq', '$regA', '$regB', '$Ly'),
                   S('label', '$Lx'),
                   bar])
                   
    def test_optimize_global_bne_j_false(self):
        foo = S('command', 'foo')
        bar = S('command', 'bar')
        
        arguments = [foo, \
                     S('command', 'bne', '$regA', '$regB', '$Lz'), \
                     S('command', 'j', '$Ly'), \
                     S('label', '$Lx'), \
                     bar]
        block = B(arguments)
        optimize_global(block)
        
        self.assertEquals(block.statements, arguments)
        
    def test_optimize_block_move_move_true(self):
        foo = S('command', 'foo')
        bar = S('command', 'bar')
        
        block = B([foo,
                   S('command', 'move', '$regA', '$regB'),
                   S('command', 'move', '$regB', '$regA'),
                   bar])
        optimize_block(block)
        
        self.assertEquals(block.statements, [foo,
                   S('command', 'move', '$regA', '$regB'),
                   bar])
                   
    def test_optimize_block_mov_mov_false(self):
        foo = S('command', 'foo')
        bar = S('command', 'bar')
        
        arguments = [foo, \
                     S('command', 'move', '$regA', '$regB'), \
                     S('command', 'move', '$regB', '$regC'), \
                     bar]
        block = B(arguments)
        optimize_block(block)
        
        self.assertEquals(block.statements, arguments)
        
    def test_optimize_blocks(self):
        foo = S('command', 'foo')
        bar = S('command', 'bar')
        
        block1 = B([foo, bar])
        block2 = B([bar, foo])
        blocks_in = [block1, block2];
        
        blocks_out = optimize_blocks(blocks_in)
        
        self.assertEquals(blocks_in, blocks_out)
