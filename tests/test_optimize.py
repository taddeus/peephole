import unittest

from src.optimize import optimize_global
from src.statement import Statement as S, Block as B


class TestOptimize(unittest.TestCase):

    def setUp(self):
        pass

    def test_optimize_global_movaa(self):
        foo = S('command', 'foo')
        bar = S('command', 'baz')
        block = B([foo, \
                   S('command', 'move', '$regA', '$regA'),
                   bar])
        optimize_global(block)
        self.assertEquals(block.statements, [foo, bar]) 
