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
