import unittest

from src.statement import Statement as S
from src.dataflow import BasicBlock as B, find_leaders, find_basic_blocks, \
        generate_flow_graph, Dag, DagNode, DagLeaf, get_defs, \
        reaching_definitions


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

    def test_get_defs(self):
        s1 = S('command', 'add', '$3', '$1', '$2')
        s2 = S('command', 'move', '$1', '$3')
        s3 = S('command', 'move', '$3', '$2')
        s4 = S('command', 'li', '$4', '0x00000001')
        block = B([s1, s2, s3, s4])
        self.assertEqual(get_defs([block]), {
            '$3': set([s1.sid, s3.sid]),
            '$1': set([s2.sid]),
            '$4': set([s4.sid])
        })

    def test_create_gen_kill_simple(self):
        s1 = S('command', 'addu', '$3', '$1', '$2')
        s2 = S('command', 'addu', '$1', '$3', 10)
        s3 = S('command', 'subu', '$3', '$1', 5)
        s4 = S('command', 'li', '$4', '0x00000001')
        block = B([s1, s2, s3, s4])
        block.create_gen_kill(get_defs([block]))
        self.assertEqual(block.gen_set, set([s2.sid, s3.sid, s4.sid]))
        self.assertEqual(block.kill_set, set([s1.sid]))


    def test_create_gen_kill_between_blocks(self):
        s11 = S('command', 'li', 'a', 3)
        s12 = S('command', 'li', 'b', 5)
        s13 = S('command', 'li', 'd', 4)
        s14 = S('command', 'li', 'x', 100)
        s15 = S('command', 'blt', 'a', 'b', 'L1')
        b1 = B([s11, s12, s13, s14, s15])

        s21 = S('command', 'addu', 'c', 'a', 'b')
        s22 = S('command', 'li', 'd', 2)
        b2 = B([s21, s22])

        s31 = S('label', 'L1')
        s32 = S('command', 'li', 'c', 4)
        s33 = S('command', 'mult', 'b', 'd')
        s34 = S('command', 'mflo', 'temp')
        s35 = S('command', 'addu', 'return', 'temp', 'c')
        b3 = B([s31, s32, s33, s34, s35])

        defs = get_defs([b1, b2, b3])
        b1.create_gen_kill(defs)
        b2.create_gen_kill(defs)
        b3.create_gen_kill(defs)

        self.assertEqual(b1.gen_set, set([s11.sid, s12.sid, s13.sid, s14.sid]))
        self.assertEqual(b1.kill_set, set([s22.sid]))

        self.assertEqual(b2.gen_set, set([s21.sid, s22.sid]))
        self.assertEqual(b2.kill_set, set([s13.sid, s32.sid]))

        self.assertEqual(b3.gen_set, set([s32.sid, s34.sid, s35.sid]))
        self.assertEqual(b3.kill_set, set([s21.sid]))


    def test_reaching_definitions(self):
        s11 = S('command', 'li', 'a', 3)
        s12 = S('command', 'li', 'b', 5)
        s13 = S('command', 'li', 'd', 4)
        s14 = S('command', 'li', 'x', 100)
        s15 = S('command', 'blt', 'a', 'b', 'L1')
        b1 = B([s11, s12, s13, s14, s15])

        s21 = S('command', 'addu', 'c', 'a', 'b')
        s22 = S('command', 'li', 'd', 2)
        b2 = B([s21, s22])

        s31 = S('label', 'L1')
        s32 = S('command', 'li', 'c', 4)
        s33 = S('command', 'mult', 'b', 'd')
        s34 = S('command', 'mflo', 'temp')
        s35 = S('command', 'addu', 'return', 'temp', 'c')
        b3 = B([s31, s32, s33, s34, s35])

        reaching_definitions([b1, b2, b3])
        self.assertEqual(b1.in_set, set())
        self.assertEqual(b1.out_set, set([s11.sid, s12.sid, s13.sid]))
        self.assertEqual(b2.in_set, set([s11.sid, s12.sid]))
        self.assertEqual(b2.out_set, set([s12.sid, s22.sid]))
        self.assertEqual(b3.in_set, set([s12.sid, s22.sid]))
        self.assertEqual(b3.out_set, set())

    def test_generate_flow_graph_simple(self):
        b1 = B([S('command', 'foo'), S('command', 'j', 'b2')])
        b2 = B([S('label', 'b2'), S('command', 'bar')])
        generate_flow_graph([b1, b2])

        self.assertEqual(b1.edges_to, [b2])
        self.assertEqual(b2.edges_from, [b1])

    def test_generate_flow_graph_branch(self):
        b1 = B([S('command', 'foo'), S('command', 'beq', '$1', '$2', 'b3')])
        b2 = B([S('command', 'bar')])
        b3 = B([S('label', 'b3'), S('command', 'baz')])
        generate_flow_graph([b1, b2, b3])

        self.assertIn(b2, b1.edges_to)
        self.assertIn(b3, b1.edges_to)
        self.assertEqual(b2.edges_from, [b1])
        self.assertEqual(b2.edges_to, [b3])
        self.assertIn(b1, b3.edges_from)
        self.assertIn(b2, b3.edges_from)

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
