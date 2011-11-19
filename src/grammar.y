%{
#include <stdio.h>
#include <stdlib.h>

// Instruction types
#define TYPE_COMMENT 0
#define TYPE_DIRECTIVE 1
#define TYPE_LABEL 2
#define TYPE_CMD 3

// Argument types
#define ARG_INT 0
#define ARG_REG 1
#define ARG_LABEL 2
#define ARG_OFFSET 3

typedef struct line {
    int type;
    const char *name;
    int argc;
    char **argv;
    int *argt;

    struct line *prev;
    struct line *next;
} line;

void yyerror(char*);
void add_line(int type, const char *name, int argc, char **argv, int *argt);

line *first_line, *last_line;

%}

%union {
    int ival;
    char *sval;
}

%token NL COMMA
%token <ival> INT
%token <sval> COMMENT DIRECTIVE WORD LABEL OFFSET CMD
%start symbol

%type <sval> command

%%

command:
    "add" WORD COMMA WORD COMMA WORD {
        char **argv = (char **)malloc(3 * sizeof(char *));
        int *argt = (int *)malloc(3 * sizeof(int));
        argv[0] = $2;
        argv[1] = $4;
        argv[2] = $6;
        argt[2] = argt[1] = argt[0] = ARG_REG;
        add_line(TYPE_CMD, "add", 3, argv, argt);
    }
    ;

symbol:
    symbol symbol
    | COMMENT   { printf("Found comment: %s\n", $1); }
    | DIRECTIVE { printf("Found directive: %s\n", $1); }
    | WORD      { printf("Found word: %s\n", $1); }
    | LABEL     { printf("Found label: %s\n", $1); }
    | INT       { printf("Found integer: %d\n", $1); }
    | OFFSET    { printf("Found offset registry address: %s\n", $1); }
    | CMD       { printf("Found command: %s\n", $1); }
    | COMMA     { printf("Found comma\n"); }
    | NL        { printf("Found newline\n"); }
    ;
%%

extern int yylex();
extern int yyparse();
extern FILE *yyin;

main(int argc, const char *argv[])
{
    if( argc < 2 ) {
        printf("No file specified");
        exit(-1);
    }

    // open a file handle to a particular file:
	FILE *myfile = fopen(argv[1], "r");
	// make sure it is valid:
	if( !myfile ) {
		printf("Cannot open %s\n", argv[1]);
		return -1;
	}
	// set lex to read from it instead of defaulting to STDIN:
	yyin = myfile;

	// parse through the input until there is no more:
	do {
		yyparse();
	} while( !feof(yyin) );
}

void yyerror(char *s)
{
    printf("Error: %s\n", s);
    exit(1);
}

void add_line(int type, const char *name, int argc, char **argv, int *argt) {
    line *l = (line*)malloc(sizeof(line));
    printf("\nName: %s\n\n", name);

    l->argc = argc;
    l->argv = argv;
    l->argt = argt;

    if( last_line == NULL ) {
        // First line
        first_line = last_line = l;
    } else {
        // Add line to linked list
        l->prev = last_line;
        last_line = last_line->next = l;
    }
}
