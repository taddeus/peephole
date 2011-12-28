import unittest

from src.statement import Statement as S
from src.dataflow import BasicBlock as B, find_leaders, find_basic_blocks, \
        generate_flow_graph


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
                 
#    def test_get_gen(self):
#        b1 = B([S('command', 'add', '$1', '$2', '$3'), \
#                S('command', 'add', '$2', '$3', '$4'), \
#                S('command', 'add', '$1', '$4', '$5')])
#        
#        self.assertEqual(b1.get_gen(), ['$1', '$2'])

#    def test_get_out(self):
#        b1 = B([S('command', 'add', '$1', '$2', '$3'), \
#                S('command', 'add', '$2', '$3', '$4'), \
#                S('command', 'add', '$1', '$4', '$5'), \
#                S('command', 'j', 'b2')])
#        
#        b2 = B([S('command', 'add', '$3', '$5', '$6'), \
#                S('command', 'add', '$1', '$2', '$3'), \
#                S('command', 'add', '$6', '$4', '$5')])      
#                
#        blocks = [b1, b2]
#        
#        for block in blocks:
#            block.out_set = block.get_gen()
#            print 'block.out_set', block.out_set       

#        generate_flow_graph(blocks)     
#        print b1.get_gen()
#        print b2.get_gen()
#        print b2.get_out()


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
