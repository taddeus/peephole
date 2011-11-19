CC=gcc
LEX=lex
YACC=yacc
CFLAGS=-ll

parser: yacc lex
	$(CC) -c lex.yy.c y.tab.c
	$(CC) -o $@ lex.yy.o y.tab.o $(CFLAGS)

lex: lex.l
	$(LEX) lex.l

yacc: grammar.y
	$(YACC) -d grammar.y

all: parser
