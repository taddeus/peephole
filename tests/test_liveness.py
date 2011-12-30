import unittest

from src.statement import Statement as S
from src.dataflow import BasicBlock as B, find_basic_blocks, \
        generate_flow_graph
from src.liveness import create_use_def, create_in_out


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

        create_use_def(block)

        self.assertEqual(block.use_set, set(['$1', '$2']))
        self.assertEqual(block.def_set, set(['$3', '$4']))

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

        self.assertEqual(b1.use_set, set())
        self.assertEqual(b1.def_set, set(['a', 'b', 'd', 'x']))

        self.assertEqual(b2.use_set, set(['a', 'b']))
        self.assertEqual(b2.def_set, set(['c', 'd']))

        self.assertEqual(b3.use_set, set(['b', 'd']))
        self.assertEqual(b3.def_set, set(['c', 'temp', 'return']))

        self.assertEqual(b1.live_in, set(['$4', '$5', '$6', '$7']))
        self.assertEqual(b1.live_out, set(['a', 'b', 'd', '$4', '$5', '$6', '$7']))
        self.assertEqual(b2.live_in, set(['a', 'b', '$4', '$5', '$6', '$7']))
        self.assertEqual(b2.live_out, set(['b', 'd', '$4', '$5', '$6', '$7']))
        self.assertEqual(b3.live_in, set(['b', 'd', '$4', '$5', '$6', '$7']))
        self.assertEqual(b3.live_out, set(['$4', '$5', '$6', '$7']))
        
    def test_create_in_out_two(self):    
        s11 = S('command', 'subu', 'i', 'm', '0x00000001')
        s12 = S('command', 'move', 'j', 'n')
        s13 = S('command', 'move', 'a', 'u1')
        s14 = S('command', 'subu', 'i', 'm', '0x00000005')
        s15 = S('command', 'j', 'L1')
        
        s21 = S('label', 'L1')
        s22 = S('command', 'addi', 'i', '0x00000001')
        s23 = S('command', 'subi', 'j', '0x00000002')
        s24 = S('command', 'bnq', 'i', 'j', 'L2')
        
        s31 = S('command', 'move', 'a', 'u2')
        s32 = S('command', 'j', 'L1')        

        s41 = S('label', 'L2')
        s42 = S('command', 'move', 'i', 'u3')
        s43 = S('command', 'beq', 'g', 'd', 'L3')
        
        s51 = S('label', 'L3')
        s52 = S('command', 'addu', 'b', 'i', 'a')
        
        blocks = find_basic_blocks([s11, s12, s13, s14, s15, 
        s21, s22, s23, s24, s31, s32, s41, s42, s43, s51])
    
        generate_flow_graph(blocks)
        create_in_out(blocks)
        
        for i, block in enumerate(blocks):
            print 'block ', i,':\n\t in:', block.live_in
            print  '\t out:', block.live_out
        
        
        
        
        
        
        

