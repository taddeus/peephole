import unittest

from src.statement import Statement as S
from src.dataflow import BasicBlock as B, find_basic_blocks, \
        generate_flow_graph
from src.reaching_definitions import get_defs, create_gen_kill, create_in_out


class TestReachingDefinitions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

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

    def test_create_gen_kill(self):
        s1 = S('command', 'addu', '$3', '$1', '$2')
        s2 = S('command', 'addu', '$1', '$3', 10)
        s3 = S('command', 'subu', '$3', '$1', 5)
        s4 = S('command', 'li', '$4', '0x00000001')
        block = B([s1, s2, s3, s4])

        create_gen_kill(block, get_defs([block]))

        self.assertEqual(block.gen_set, set([s2.sid, s3.sid, s4.sid]))
        self.assertEqual(block.kill_set, set([s1.sid]))

    def test_create_in_out(self):
        s11 = S('command', 'li', 'a', 3)
        s12 = S('command', 'li', 'b', 5)
        s13 = S('command', 'li', 'd', 4)
        s14 = S('command', 'li', 'x', 100)
        s15 = S('command', 'beq', 'a', 'b', 'L1')

        s21 = S('command', 'addu', 'c', 'a', 'b')
        s22 = S('command', 'li', 'd', 2)

        s31 = S('label', 'L1')
        s32 = S('command', 'li', 'c', 4)
        s33 = S('command', 'mult', 'b', 'd')
        s34 = S('command', 'mflo', 'temp')
        s35 = S('command', 'addu', 'return', 'temp', 'c')

        b1, b2, b3, b4 = find_basic_blocks([s11, s12, s13, s14, s15, s21, s22, \
                                        s31, s32, s33, s34, s35])

        generate_flow_graph([b1, b2, b3, b4])
        create_in_out([b1, b2, b3, b4])

        self.assertEqual(b1.gen_set, set([s11.sid, s12.sid, s13.sid,
                                            s14.sid]))
        self.assertEqual(b1.kill_set, set([s22.sid]))
        self.assertEqual(b2.gen_set, set([s21.sid, s22.sid]))
        self.assertEqual(b2.kill_set, set([s13.sid, s32.sid]))
        self.assertEqual(b3.gen_set, set([s32.sid, s34.sid, s35.sid]))
        self.assertEqual(b3.kill_set, set([s21.sid]))

        self.assertEqual(b1.reach_in, set())
        self.assertEqual(b1.reach_out, set([s11.sid, s12.sid, s13.sid,
                                            s14.sid]))
        self.assertEqual(b2.reach_in, set([s11.sid, s12.sid, s13.sid,
                                            s14.sid]))
        self.assertEqual(b2.reach_out, set([s21.sid, s22.sid, s11.sid, \
                                            s12.sid, s14.sid]))
        self.assertEqual(b3.reach_in, set([s21.sid, s22.sid, s11.sid, \
                                            s12.sid, s13.sid, s14.sid]))
        self.assertEqual(b3.reach_out, set([s32.sid, s34.sid, s35.sid, \
                                            s22.sid, s11.sid, s12.sid, \
                                            s13.sid, s14.sid]))
