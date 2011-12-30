import unittest

from src.statement import Statement as S, Block as B


class TestStatement(unittest.TestCase):

    def setUp(self):
        self.statement = S('command', 'foo', '$1')
        self.block = B([S('command', 'foo'), \
                        S('comment', 'bar'),
                        S('command', 'baz')])

    def tearDown(self):
        del self.block

    def test_getitem(self):
        self.assertEqual(self.statement[0], '$1')

    def test_setitem(self):
        self.statement[0] = '$2'
        self.assertEqual(self.statement[0], '$2')

    def test_eq(self):
        self.assertTrue(S('command', 'foo') == S('command', 'foo'))
        self.assertFalse(S('command', 'foo') == S('command', 'bar'))

    def test_stype(self):
        self.assertTrue(S('comment', 'foo', inline=False).is_comment())
        self.assertTrue(S('directive', 'foo').is_directive())
        self.assertTrue(S('label', 'foo').is_label())
        self.assertTrue(S('command', 'foo').is_command())

        self.assertFalse(S('command', 'foo').is_comment())
        self.assertFalse(S('label', 'foo').is_directive())
        self.assertFalse(S('comment', 'foo', inline=False).is_label())
        self.assertFalse(S('directive', 'foo').is_command())

    def test_has_inline_comment(self):
        self.assertTrue(S('comment', 'foo', comment='a').has_inline_comment())
        self.assertFalse(S('comment', 'foo', comment='').has_inline_comment())
        self.assertFalse(S('comment', 'foo').has_inline_comment())

    def test_jump_target(self):
        self.assertEqual(S('command', 'j', 'foo').jump_target(), 'foo')
        self.assertRaises(Exception, S('command', 'foo').jump_target)

    def test_iter(self):
        self.assertEqual(self.block.statements, list(self.block))

    def test_read(self):
        self.assertEqual(self.block.read(), S('command', 'foo'))
        self.assertEqual(self.block.read(), S('comment', 'bar'))
        self.assertEqual(self.block.read(), S('command', 'baz'))

    def test_end(self):
        self.assertFalse(self.block.end())
        self.block.read()
        self.block.read()
        self.block.read()
        self.assertTrue(self.block.end())

    def test_peek(self):
        self.assertEqual(self.block.peek(), S('command', 'foo'))
        self.assertEqual(self.block.peek(2), [S('command', 'foo'), \
                                              S('comment', 'bar')])
        self.block.read()
        self.assertEqual(self.block.peek(), S('comment', 'bar'))

    def test_replace(self):
        self.block.read()
        self.block.replace(1, [S('command', 'foobar')])
        self.assertEqual(self.block.pointer, 1)
        self.assertEqual(self.block.statements, [S('command', 'foobar'), \
                                                 S('comment', 'bar'), \
                                                 S('command', 'baz')])

    def test_apply_filter(self):
        self.block.apply_filter(lambda s: s.is_command())
        self.assertEqual(self.block.statements, [S('command', 'foo'), \
                                                 S('command', 'baz')])

    def test_is_shift(self):
        self.assertTrue(S('command', 'sll').is_shift())
        self.assertFalse(S('command', 'foo').is_shift())
        self.assertFalse(S('label', 'sll').is_shift())

    def test_is_load(self):
        self.assertTrue(S('command', 'lw').is_load())
        self.assertFalse(S('command', 'foo').is_load())
        self.assertFalse(S('label', 'lw').is_load())

    def test_is_arith(self):
        self.assertTrue(S('command', 'addu', '$1', '$2', '$3').is_arith())
        self.assertFalse(S('command', 'foo').is_arith())
        self.assertFalse(S('label', 'addu').is_arith())

    def test_get_def_true(self):
        a = ['a']

        self.assertEqual(S('command', 'move', 'a', 'b').get_def(), a)
        self.assertEqual(S('command', 'subu', 'a', 'b', 'c').get_def(), a)
        self.assertEqual(S('command', 'addu', 'a', 'b', 'c').get_def(), a)
        self.assertEqual(S('command', 'div', 'a', 'b', 'c').get_def(), a)
        self.assertEqual(S('command', 'sll', 'a', 'b', 'c').get_def(), a)
        self.assertEqual(S('command', 'srl', 'a', 'b', 'c').get_def(), a)
        self.assertEqual(S('command', 'la', 'a', '16($fp)').get_def(), a)
        self.assertEqual(S('command', 'li', 'a', '16($fp)').get_def(), a)
        self.assertEqual(S('command', 'lw', 'a', 'b').get_def(), a)
        self.assertEqual(S('command', 'l.d', 'a', 'b').get_def(), a)
        self.assertEqual(S('command', 'add.d', 'a', 'b', 'c').get_def(), a)
        self.assertEqual(S('command', 'neg.d', 'a', 'b').get_def(), a)
        self.assertEqual(S('command', 'sub.d', 'a', 'b', 'c').get_def(), a)
        self.assertEqual(S('command', 'slt', 'a', 'b').get_def(), a)
        self.assertEqual(S('command', 'xori', 'a', 'b', '0x0000').get_def(), a)
        self.assertEqual(S('command', 'mov.d', 'a', 'b').get_def(), a)
        self.assertEqual(S('command', 'dmfc1', 'a', '$f0').get_def(), a)
        self.assertEqual(S('command', 'mtc1', 'b', 'a').get_def(), a)
        self.assertEqual(S('command', 'trunc.w.d', 'a', 'b', 'c').get_def(), a)

    def test_get_def_false(self):
        self.assertEqual(S('command', 'bne', 'a', 'b', 'L1').get_def(), [])
        self.assertEqual(S('command', 'beq', 'a', 'b', 'L1').get_def(), [])

    def test_get_use_true(self):
        arg1 = set()
        arg1.add('$1')
        arg2 = set()
        arg2.add('$1')
        arg2.add('$2')

        self.assertEqual(S('command', 'addu', '$3', '$1', '$2').get_use(), \
                arg2)
        self.assertEqual(S('command', 'subu', '$3', '$1', '$2').get_use(), \
                arg2)
        self.assertEqual(S('command', 'mult', '$1', '$2').get_use(), arg2)
        self.assertEqual(S('command', 'div', '$3', '$1', '$2').get_use(), arg2)
        self.assertEqual(S('command', 'move', '$2', '$1').get_use(), arg1)
        self.assertEqual(S('command', 'beq', '$1', '$2', '$L1').get_use(), \
                arg2)
        self.assertEqual(S('command', 'bne', '$1', '$2', '$L1').get_use(), \
                arg2)
        self.assertEqual(S('command', 'sll', '$2', '$1', 2).get_use(), arg1)
        self.assertEqual(S('command', 'lb', '$2', '10($1)').get_use(), arg1)
        self.assertEqual(S('command', 'lw', '$2', '10($1)').get_use(), arg1)
        self.assertEqual(S('command', 'la', '$2', '10($1)').get_use(), arg1)
        self.assertEqual(S('command', 'lb', '$2', 'n.7').get_use(), ['n.7'])
        self.assertEqual(S('command', 'lbu', '$2', '10($1)').get_use(), arg1)
        self.assertEqual(S('command', 'l.d', '$2', '10($1)').get_use(), arg1)
        self.assertEqual(S('command', 's.d', '$1', '10($2)').get_use(), \
                arg2)
        self.assertEqual(S('command', 's.s', '$1', '10($2)').get_use(), \
                arg2)
        self.assertEqual(S('command', 'sw', '$1', '10($2)').get_use(), \
                arg2)
        self.assertEqual(S('command', 'sb', '$1', '10($2)').get_use(), \
                arg2)
        self.assertEqual(S('command', 'mtc1', '$1', '$2').get_use(), arg1)
        self.assertEqual(S('command', 'add.d', '$3', '$1', '$2').get_use(), \
                arg2)
        self.assertEqual(S('command', 'sub.d', '$3', '$1', '$2').get_use(), \
                arg2)
        self.assertEqual(S('command', 'div.d', '$3', '$1', '$2').get_use(), \
                arg2)
        self.assertEqual(S('command', 'mul.d', '$3', '$1', '$2').get_use(), \
                arg2)
        self.assertEqual(S('command', 'neg.d', '$2', '$1').get_use(), arg1)
        self.assertEqual(S('command', 'abs.d', '$2', '$1').get_use(), arg1)
        self.assertEqual(S('command', 'dsz', '10($1)', '$2').get_use(), arg1)
        self.assertEqual(S('command', 'dsw', '$1', '10($2)').get_use(), arg2)
        self.assertEqual(S('command', 'c.lt.d', '$1', '$2').get_use(), arg2)
        self.assertEqual(S('command', 'bgez', '$1', '$2').get_use(), arg1)
        self.assertEqual(S('command', 'bltz', '$1', '$2').get_use(), arg1)
        self.assertEqual(S('command', 'trunc.w.d', '$3', '$1', '$2').get_use(),
                         arg2)
