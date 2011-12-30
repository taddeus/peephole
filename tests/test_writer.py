import unittest

from src.writer import write_statements
from src.statement import Statement as S, Block as B


class TestWriter(unittest.TestCase):

    def setUp(self):
        self.foo = S('command', 'move', '$regA', '$regB')
        self.bar = S('command', 'addu', '$regC', '$regA', '$regB')

    def tearDown(self):
        del self.foo
        del self.bar
        
    def test_writer_one(self):
        output = write_statements([self.foo])
        expect = "\tmove\t$regA,$regB\n"
        self.assertEqual(output, expect)
        
    def test_writer_longname(self):
        command = S('command', 'movemovemove', '$regA', '$regB')
        output = write_statements([command])
        expect = "\tmovemovemove $regA,$regB\n"
        self.assertEqual(output, expect)
        
    def test_writer_several(self):
        output = write_statements([self.foo, self.bar, self.foo])
        expect = "\tmove\t$regA,$regB\n" \
                 + "\taddu\t$regC,$regA,$regB\n" \
                 + "\tmove\t$regA,$regB\n"
        self.assertEqual(output, expect)
        
    def test_writer_with_label(self):
        label = S('label', '$L1')
        output = write_statements([self.foo, label, self.bar])
        expect = "\tmove\t$regA,$regB\n" \
                 + "$L1:\n" \
                 + "\taddu\t$regC,$regA,$regB\n"
        self.assertEqual(output, expect)
        
    def test_writer_with_comment(self):
        comment = S('comment', 'tralala')
        output = write_statements([self.foo, comment, self.bar])
        expect = "\tmove\t$regA,$regB\n" \
                 + "\n#tralala\n\n" \
                 + "\taddu\t$regC,$regA,$regB\n"
        self.assertEqual(output, expect)
        
    def test_writer_with_comment_non_tabbed(self):
        directive = S('comment', 'tralala')
        output = write_statements([directive, self.foo, self.bar])
        expect = "\n#tralala\n\n" \
                 + "\tmove\t$regA,$regB\n" \
                 + "\taddu\t$regC,$regA,$regB\n"
        self.assertEqual(output, expect)
        
    def test_writer_with_inlinecomment(self):
        self.foo.options['comment'] = 'tralala'
        output = write_statements([self.foo, self.bar])
        expect = "\tmove\t$regA,$regB" \
                 + "\t\t#tralala\n" \
                 + "\taddu\t$regC,$regA,$regB\n"
        self.assertEqual(output, expect)
        
    def test_writer_with_directive(self):
        directive = S('directive', '.tralala trololo')
        output = write_statements([self.foo, directive, self.bar])
        expect = "\tmove\t$regA,$regB\n" \
                 + "\t.tralala trololo\n" \
                 + "\taddu\t$regC,$regA,$regB\n"
        self.assertEqual(output, expect)
