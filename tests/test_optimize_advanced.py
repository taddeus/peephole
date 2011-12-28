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
        print "testing true"
        block = B([self.foo,
                   S('command', 'move', '$1', '$2'),
                   self.foo,
                   S('command', 'addu', '$3', '$1', '$4'),
                   self.bar])
                   
        copy_propagation(block)
        self.assertEqual(block.statements, [self.foo,
                   S('command', 'move', '$1', '$2'),
                   self.foo,
                   S('command', 'addu', '$3', '$2', '$4'),
                   self.bar])
        print "Test true succesfull"
                   
#    def test_copy_propagation_false(self):
#        print "Testing false"
#        arguments = [self.foo,
#                   S('command', 'move', '$1', '$2'),
#                   S('command', 'move', '$10', '$20'),
#                   S('command', 'addu', '$1', '$5', 1),
#                   S('command', 'addu', '$3', '$1', '$4'),
#                   self.bar]
#        block = B(arguments)
#        copy_propagation(block)
#        self.assertEqual(block.statements, arguments)
