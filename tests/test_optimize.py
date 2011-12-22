import unittest

from src.optimize import optimize_global
from src.statement import Statement as S, Block as B


class TestOptimize(unittest.TestCase):

    def setUp(self):
        pass

    def test_optimize_global_movaa(self):
        foo = S('command', 'foo')
        bar = S('command', 'bar')
        block = B([foo,
                   S('command', 'move', '$regA', '$regA'),
                   bar])
        optimize_global(block)
        self.assertEquals(block.statements, [foo, bar])
        
    def test_optimize_global_movab(self):
        foo = S('command', 'foo')
        move = S('command', 'move', '$regA', '$regB')
        bar = S('command', 'bar')
        block = B([foo,
                   move,
                   bar])
        optimize_global(block)
        self.assertEquals(block.statements, [foo, move, bar])
        
    def test_optimize_global_movinst_true(self):
        foo = S('command', 'foo')
        bar = S('command', 'bar')
        
        block = B([foo,
                   S('command', 'move', '$regA', '$regB'),
                   S('command', 'addu', '$regA', '$regA', 2),
                   bar])
        optimize_global(block)
        self.assertEquals(block.statements, [foo,                     
                   S('command', 'addu', '$regA', '$regB', 2),      
                   bar])
                   
    def test_optimize_global_movinst_false(self):
        foo = S('command', 'foo')
        bar = S('command', 'bar')
        statements = [foo, \
                      S('command', 'move', '$regA', '$regB'), \
                      S('command', 'addu', '$regA', '$regC', 2), \
                      bar]
        
        block = B(statements)
        optimize_global(block)
        self.assertEquals(block.statements, statements)
                
    def test_optimize_global_instr_mov_jal_true(self):
        foo = S('command', 'foo')
        bar = S('command', 'bar')
        
        block = B([foo,
                   S('command', 'addu', '$regA', '$regC', 2),
                   S('command', 'move', '$4', '$regA'),
                   S('command', 'jal', 'L1'),
                   bar])
        optimize_global(block)
        
        self.assertEquals(block.statements, [foo,                     
                   S('command', 'addu', '$4', '$regC', 2),
                   S('command', 'jal', 'L1'),      
                   bar])
        
    def test_optimize_global_instr_mov_jal_false(self):
        foo = S('command', 'foo')
        bar = S('command', 'bar')
        
        arguments = [foo, \
                      S('command', 'addu', '$regA', '$regC', 2), \
                      S('command', 'move', '$3', '$regA'), \
                      S('command', 'jal', 'L1'), \
                      bar]
        block = B(arguments)
        optimize_global(block)
        
        self.assertEquals(block.statements, arguments)
        
    def test_optimize_global_sw_ld_true(self):
        foo = S('command', 'foo')
        bar = S('command', 'bar')
        
        block = B([foo,
                   S('command', 'sw', '$regA', '$regB'),
                   S('command', 'ld', '$regA', '$regC'),
                   bar])
        optimize_global(block)
        
        self.assertEquals(block.statements, [foo,
                   S('command', 'sw', '$regA', '$regB'),
                   bar])
                   
    def test_optimize_global_sw_ld_false(self):
        foo = S('command', 'foo')
        bar = S('command', 'bar')
        
        arguments = [foo, \
                     S('command', 'sw', '$regA', '$regB'), \
                     S('command', 'ld', '$regD', '$regC'), \
                     bar]
        block = B(arguments)
        optimize_global(block)
        
        self.assertEquals(block.statements, arguments)
