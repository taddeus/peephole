import unittest
from copy import copy

from src.optimize.advanced import eliminate_common_subexpressions, \
        fold_constants, copy_propagation, algebraic_transformations
from src.statement import Statement as S, Block as B


class TestOptimizeAdvanced(unittest.TestCase):

    def setUp(self):
        self.foo = S('command', 'foo')
        self.bar = S('command', 'bar')

    def tearDown(self):
        del self.foo
        del self.bar

    def test_eliminate_common_subexpressions_simple(self):
        b = B([S('command', 'addu', '$regC', '$regA', '$regB'),
               S('command', 'addu', '$regD', '$regA', '$regB')])
        e = [S('command', 'addu', '$t0', '$regA', '$regB'), \
             S('command', 'move', '$regC', '$t0'), \
             S('command', 'move', '$regD', '$t0')]
        eliminate_common_subexpressions(b)
        self.assertEqual(b.statements, e)

    def test_eliminate_common_subexpressions_assigned(self):
        b = B([S('command', 'addu', '$regC', '$regA', '$regB'),
               S('command', 'li', '$regA', '0x00000001'),
               S('command', 'addu', '$regD', '$regA', '$regB')])
        e = copy(b.statements)
        eliminate_common_subexpressions(b)
        self.assertEqual(b.statements, e)

    def test_fold_constants(self):
        pass

    def test_copy_propagation_true(self):
        block = B([self.foo,
                   S('command', 'move', '$1', '$2'),
                   self.foo,
                   S('command', 'addu', '$3', '$1', '$4'),
                   self.bar])

        self.assertTrue(copy_propagation(block))
        self.assertEqual(block.statements, [self.foo,
                   S('command', 'move', '$1', '$2'),
                   self.foo,
                   S('command', 'addu', '$3', '$2', '$4'),
                   self.bar])

    def test_copy_propagation_overwrite(self):
        block = B([self.foo, \
                    S('command', 'move', '$1', '$2'),
                    S('command', 'move', '$1', '$5'),
                    S('command', 'addu', '$3', '$1', '$4'),
                    self.bar])

        self.assertTrue(copy_propagation(block))
        self.assertEqual(block.statements, [self.foo,
                   S('command', 'move', '$1', '$2'),
                   S('command', 'move', '$1', '$5'),
                   S('command', 'addu', '$3', '$5', '$4'),
                   self.bar])

    def test_copy_propagation_false(self):
        arguments = [self.foo,
                   S('command', 'move', '$1', '$2'),
                   S('command', 'move', '$10', '$20'),
                   S('command', 'addu', '$1', '$5', 1),
                   S('command', 'addu', '$3', '$1', '$4'),
                   self.bar]
        block = B(arguments)
        self.assertFalse(copy_propagation(block))
        self.assertEqual(block.statements, arguments)

    def test_copy_propagation_false_severalmoves(self):
        arguments = [self.foo,
                   S('command', 'move', '$1', '$2'),
                   self.foo,
                   S('command', 'addu', '$1', '$5', 1),
                   S('command', 'addu', '$3', '$1', '$4'),
                   self.bar]
        block = B(arguments)
        self.assertFalse(copy_propagation(block))
        self.assertEqual(block.statements, arguments)

    def test_algebraic_transforms_add0(self):
        block = B([self.foo,
                   S('command', 'addu', '$1', '$2', 0),
                   self.bar])

#        self.assertTrue(copy_propagation(block))
        algebraic_transformations(block)
        self.assertEqual(block.statements, [self.foo,
                   self.bar])
