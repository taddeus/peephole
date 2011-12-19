import unittest

from src.utils import Statement as S, Block as B, find_leaders, \
        find_basic_blocks


class TestUtils(unittest.TestCase):

    def setUp(self):
        pass

    def test_find_leaders(self):
        add = S('command', 'add', '$1', '$2', '$3')
        s = [add, S('command', 'j', 'foo'), add, add, S('label', 'foo')]
        self.assertEqual(find_leaders(s), [0, 2, 4])

    def test_find_basic_blocks(self):
        add = S('command', 'add', '$1', '$2', '$3')
        s = [add, S('command', 'j', 'foo'), add, add, S('label', 'foo')]
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
