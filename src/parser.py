#!/usr/bin/python
import ply.lex as lex
import ply.yacc as yacc

tokens = ('NEWLINE', 'WORD', 'COMMENT', 'DIRECTIVE', 'COMMA', 'COLON')

# Tokens
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')
    return t

def t_COLON(t):
    r':'
    return t

def t_COMMA(t):
    r','
    return t

def t_COMMENT(t):
    r'\#.*'
    return t

def t_DIRECTIVE(t):
    r'\..*'
    return t

def t_offset_address(t):
    r'[0-9]+(\([a-zA-Z0-9$_.]+\))?'
    t.type = 'WORD'
    return t

def t_WORD(t):
    r'[a-zA-Z0-9$_.]+'
    return t

# Ignore whitespaces
t_ignore = ' \t'

def t_error(t):
    print('Illegal character "%s"' % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Parsing rules
precedence = (
    ('nonassoc', 'COLON', 'COMMA'),
    ('nonassoc', 'COMMENT', 'DIRECTIVE'),
    ('nonassoc', 'WORD'),
    )

def p_input(p):
    '''input :
             | input line'''
    pass

def p_line_instruction(p):
    'line : instruction NEWLINE'
    pass

def p_line_comment(p):
    'line : COMMENT NEWLINE'
    print 'comment line', list(p)[1:]

def p_line_inline_comment(p):
    'line : instruction COMMENT NEWLINE'
    print 'inline comment', list(p)[1:]

def p_instruction_command(p):
    'instruction : command'
    pass

def p_instruction_directive(p):
    'instruction : DIRECTIVE'
    print 'directive', list(p)[1:]

def p_instruction_label(p):
    'instruction : WORD COLON'
    print 'label', list(p)[1:]

def p_command_3(p):
    'command : WORD WORD COMMA WORD COMMA WORD'
    print 'command with 3 args', list(p)[1:]

def p_command_2(p):
    'command : WORD WORD COMMA WORD'
    print 'command with 2 args', list(p)[1:]

def p_command_1(p):
    'command : WORD WORD'
    print 'command with 1 args', list(p)[1:]

def p_error(p):
    print 'Syntax error at "%s"' % p.value

yacc.yacc()
yacc.parse(open('hello.s').read())

#lexer.input(open('hello.s').read())
#
#while True:
#    tok = lexer.token()
#
#    if not tok:
#        break
#
#    print tok

#while 1:
    #try:
    #    s = input('calc > ')  # Use raw_input on Python 2
    #except EOFError:
    #    break
    #yacc.parse(s)
