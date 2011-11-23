CC=gcc
LEX=lex
YACC=yacc

CFLAGS = -std=c99 -pedantic -Wall -D_POSIX_SOURCE -D_GNU_SOURCE $(PIC) -pipe

all: peephole

peephole: y.tab.o lex.yy.o
	$(CC) -o $@ $^ -lm

y.tab.c y.tab.h: peephole.y
	$(YACC) -d $^

lex.yy.c: peephole.l
	$(LEX) $^

clean:
	rm -f lex.yy.* y.tab.* *.o peephole
