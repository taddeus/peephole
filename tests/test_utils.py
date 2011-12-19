import unittest

from src.utils import Statement as S, Block as B, find_leaders, \
        find_basic_blocks


class TestUtils(unittest.TestCase):

    def setUp(self):
        add = S('command', 'add', '$1', '$2', '$3')
        self.statements = [add, S('command', 'j', 'foo'), add, add, \
                S('label', 'foo')]
        self.block = B([S('command', 'foo'), \
                        S('comment', 'bar'),
                        S('command', 'baz')])

    def tearDown(self):
        del self.statements
        del self.block

    def test_find_leaders(self):
        self.assertEqual(find_leaders(self.statements), [0, 2, 4])

    def test_find_basic_blocks(self):
        s = self.statements
        self.assertEqual(map(lambda b: b.statements, find_basic_blocks(s)), \
                [B(s[:2]).statements, B(s[2:4]).statements, \
                 B(s[4:]).statements])

    def test_eq(self):
        self.assertTrue(S('command', 'foo') == S('command', 'foo'))
        self.assertFalse(S('command', 'foo') == S('command', 'bar'))

    def test_stype(self):
        self.assertTrue(S('comment', 'foo', inline=False).is_comment())
        self.assertTrue(S('directive', 'foo').is_directive())
        self.assertTrue(S('label', 'foo').is_label())
        self.assertTrue(S('command', 'foo').is_command())

        self.assertFalse(S('command', 'foo').is_comment())
        self.assertFalse(S('label', 'foo').is_directive())
        self.assertFalse(S('comment', 'foo', inline=False).is_label())
        self.assertFalse(S('directive', 'foo').is_command())

    def test_is_inline_comment(self):
        self.assertTrue(S('comment', 'foo', inline=True).is_inline_comment())
        self.assertFalse(S('comment', 'foo', inline=False).is_inline_comment())

    def test_jump_target(self):
        self.assertEqual(S('command', 'j', 'foo').jump_target(), 'foo')
        self.assertRaises(Exception, S('command', 'foo').jump_target)

    def test_iter(self):
        self.assertEqual(self.block.statements, list(self.block))

    def test_read(self):
        self.assertEqual(self.block.read(), S('command', 'foo'))
        self.assertEqual(self.block.read(), S('comment', 'bar'))
        self.assertEqual(self.block.read(), S('command', 'baz'))

    def test_end(self):
        self.assertFalse(self.block.end())
        self.block.read()
        self.block.read()
        self.block.read()
        self.assertTrue(self.block.end())

    def test_peek(self):
        self.assertEqual(self.block.peek(), S('command', 'foo'))
        self.assertEqual(self.block.peek(2), [S('command', 'foo'), \
                                              S('comment', 'bar')])
        self.block.read()
        self.assertEqual(self.block.peek(), S('comment', 'bar'))

    def test_replace(self):
        self.block.replace(1, [S('command', 'foobar')])
        self.assertEqual(self.block.pointer, 1)
        self.assertEqual(self.block.statements, [S('command', 'foobar'), \
                                                 S('comment', 'bar'), \
                                                 S('command', 'baz')])

    def test_apply_filter(self):
        self.block.apply_filter(lambda s: s.is_command())
        self.assertEqual(self.block.statements, [S('command', 'foo'), \
                                                 S('command', 'baz')])
