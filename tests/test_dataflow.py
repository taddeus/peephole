import unittest

from src.statement import Statement as S, Block as B
from src.dataflow import find_leaders, find_basic_blocks


class TestDataflow(unittest.TestCase):

    def setUp(self):
        add = S('command', 'add', '$1', '$2', '$3')
        self.statements = [add, S('command', 'j', 'foo'), add, add, \
                S('label', 'foo')]

    def tearDown(self):
        del self.statements

    def test_find_leaders(self):
        self.assertEqual(find_leaders(self.statements), [0, 2, 4])

    def test_find_basic_blocks(self):
        s = self.statements
        self.assertEqual(map(lambda b: b.statements, find_basic_blocks(s)), \
                [B(s[:2]).statements, B(s[2:4]).statements, \
                 B(s[4:]).statements])

