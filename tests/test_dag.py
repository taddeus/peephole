import unittest

from src.statement import Statement as S
from src.dataflow import BasicBlock as B
from src.dag import Dag, DagNode, DagLeaf


class TestDag(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_dag_unary(self):
        dag = Dag(B([S('command', 'neg.d', '$rd', '$rs')]))
        expect = Dag([])
        expect.nodes = [DagLeaf('$rs'), DagNode('neg.d', '$rd', \
                        DagLeaf('$rs'))]

        self.assertEqualDag(dag, expect)

    def test_dag_binary(self):
        dag = Dag(B([S('command', 'addu', '$rd', '$r1', '$r2')]))
        expect = Dag([])
        expect.nodes = [DagLeaf('$r1'),
                        DagLeaf('$r2'),
                        DagNode('addu', '$rd', DagLeaf('$r1'), DagLeaf('$r2'))]

        self.assertEqualDag(dag, expect)

#    def test_dag_combinednode(self):
#        dag = Dag(B([S('command', 'mult', '$rd1', '$r1', '$r2'),
#                     S('command', 'mult', '$rd2', '$r1', '$r2')]))
#        expect = Dag([])
#        multnode = DagNode('mult',
#                           DagLeaf('$r1'),
#                           DagLeaf('$r2'))
#        multnode.labels = ['$rd1', '$rd2']
#        expect.nodes = [DagLeaf('$r1'),
#                        DagLeaf('$r2'),
#                        multnode]
#
#        self.assertEqualDag(dag, expect)

    def assertEqualDag(self, dag1, dag2):
        self.assertEqual(len(dag1.nodes), len(dag2.nodes))

        for node1, node2 in zip(dag1.nodes, dag2.nodes):
            self.assertEqualNodes(node1, node2)

    def assertEqualNodes(self, node1, node2):
        if isinstance(node1, DagLeaf):
            self.assertIsInstance(node2, DagLeaf)
            self.assertEqual(node1.reg, node2.reg)
        elif isinstance(node2, DagLeaf):
            raise AssertionError
        else:
            self.assertEqual(node1.op, node2.op)
            self.assertEqual(node1.labels, node2.labels)
            self.assertEqual(len(node1.nodes), len(node2.nodes))

            for child1, child2 in zip(node1.nodes, node2.nodes):
                self.assertEqualNodes(child1, child2)
