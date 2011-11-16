CC=gcc
LEX=lex
YACC=yacc
CFLAGS=-ll

parser: yacc lex
	$(CC) -c lex.yy.c y.tab.c
	$(CC) -o $@ lex.yy.o y.tab.o $(CFLAGS)

lex: lex.l
	$(LEX) lex.l
	
yacc: lex_out.y
	$(YACC) -d lex_out.y

all: parser
