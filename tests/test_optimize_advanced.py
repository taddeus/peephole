import unittest

from src.optimize.advanced import eliminate_common_subexpressions, \
        fold_constants, copy_propagation
from src.statement import Statement as S, Block as B


class TestOptimizeAdvanced(unittest.TestCase):

    def setUp(self):
        self.foo = S('command', 'foo')
        self.bar = S('command', 'bar')

    def test_eliminate_common_subexpressions(self):
        pass

    def test_copy_propagation_true(self):
#        block = B([self.foo,
#                   S('command', 'move', '$1', '$2'),
#                   self.foo,
#                   S('command', 'addu', '$3', '$1', '$4'),
#                   self.bar])
#
#        copy_propagation(block)
#        self.assertEquals(block.statements, [self.foo,
#                   S('command', 'move', '$1', '$2'),
#                   self.foo,
#                   S('command', 'addu', '$3', '$2', '$4'),
#                   self.bar])
        pass
