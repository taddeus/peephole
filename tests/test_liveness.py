import unittest

from src.statement import Statement as S
from src.dataflow import BasicBlock as B
from src.liveness import create_gen_kill, create_in_out


class TestLiveness(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_gen_kill(self):
        s1 = S('command', 'addu', '$3', '$1', '$2')
        s2 = S('command', 'addu', '$1', '$3', 10)
        s3 = S('command', 'subu', '$3', '$1', 5)
        s4 = S('command', 'li', '$4', '0x00000001')
        block = B([s1, s2, s3, s4])

        create_gen_kill(block)

        self.assertEqual(block.live_gen, set(['$1', '$2']))
        self.assertEqual(block.live_kill, set(['$3', '$1', '$1']))

    #def test_create_in_out(self):
    #    s11 = S('command', 'li', 'a', 3)
    #    s12 = S('command', 'li', 'b', 5)
    #    s13 = S('command', 'li', 'd', 4)
    #    s14 = S('command', 'li', 'x', 100)
    #    s15 = S('command', 'blt', 'a', 'b', 'L1')
    #    b1 = B([s11, s12, s13, s14, s15])

    #    s21 = S('command', 'addu', 'c', 'a', 'b')
    #    s22 = S('command', 'li', 'd', 2)
    #    b2 = B([s21, s22])

    #    s31 = S('label', 'L1')
    #    s32 = S('command', 'li', 'c', 4)
    #    s33 = S('command', 'mult', 'b', 'd')
    #    s34 = S('command', 'mflo', 'temp')
    #    s35 = S('command', 'addu', 'return', 'temp', 'c')
    #    b3 = B([s31, s32, s33, s34, s35])

    #    create_in_out([b1, b2, b3])

    #    self.assertEqual(b1.live_gen, set([s11.sid, s12.sid, s13.sid, s14.sid]))
    #    self.assertEqual(b1.live_kill, set([s22.sid]))

    #    self.assertEqual(b2.live_gen, set([s21.sid, s22.sid]))
    #    self.assertEqual(b2.live_kill, set([s13.sid, s32.sid]))

    #    self.assertEqual(b3.live_gen, set([s32.sid, s34.sid, s35.sid]))
    #    self.assertEqual(b3.live_kill, set([s21.sid]))

    #    self.assertEqual(b1.live_in, set())
    #    self.assertEqual(b1.live_out, set([s11.sid, s12.sid, s13.sid]))
    #    self.assertEqual(b2.live_in, set([s11.sid, s12.sid]))
    #    self.assertEqual(b2.live_out, set([s12.sid, s22.sid]))
    #    self.assertEqual(b3.live_in, set([s12.sid, s22.sid]))
    #    self.assertEqual(b3.live_out, set())
