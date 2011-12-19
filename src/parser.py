import ply.lex as lex
import ply.yacc as yacc

from utils import Statement as S, Block

# Global statements administration
statements = []

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
    t.value = t.value[1:]
    return t

def t_DIRECTIVE(t):
    r'\..*'
    return t

def t_hex_word(t):
    r'0x[0-9a-fA-F]{8}'
    t.type = 'WORD'
    return t

def t_offset_address(t):
    r'[0-9]+\([a-zA-Z0-9$_.]+\)'
    t.type = 'WORD'
    return t

def t_int(t):
    r'-?[0-9]+'
    t.type = 'WORD'
    return t

def t_WORD(t):
    r'[a-zA-Z0-9$_.+()]+'
    return t

# Ignore whitespaces
t_ignore = ' \t'

def t_error(t):
    print('Illegal character "%s"' % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Parsing rules
start = 'input'

def p_input(p):
    '''input :
             | input line'''
    pass

def p_line_instruction(p):
    'line : instruction NEWLINE'
    pass

def p_line_comment(p):
    'line : COMMENT NEWLINE'
    statements.append(S('comment', p[1], inline=False))

def p_line_inline_comment(p):
    'line : instruction COMMENT NEWLINE'
    statements.append(S('comment', p[2], inline=True))

def p_instruction_command(p):
    'instruction : command'
    pass

def p_instruction_directive(p):
    'instruction : DIRECTIVE'
    statements.append(S('directive', p[1]))

def p_instruction_label(p):
    'instruction : WORD COLON'
    statements.append(S('label', p[1]))

def p_command(p):
    '''command : WORD WORD COMMA WORD COMMA WORD
               | WORD WORD COMMA WORD
               | WORD WORD
               | WORD'''
    statements.append(S('command', p[1], *list(p)[2::2]))

def p_error(p):
    print 'Syntax error at "%s" on line %d' % (p.value, lexer.lineno)

yacc.yacc()

def parse_file(filename):
    global statements

    statements = []

    try:
        content = open(filename).read()
        yacc.parse(content)
    except IOError:
        print 'File "%s" could not be opened' % filename

    return Block(statements)
