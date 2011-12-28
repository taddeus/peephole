import unittest

from src.optimize.advanced import eliminate_common_subexpressions, \
        fold_constants, copy_propagation
from src.statement import Statement as S, Block as B


class TestOptimizeAdvanced(unittest.TestCase):

    def setUp(self):
        pass

    def test_eliminate_common_subexpressions(self):
        pass
