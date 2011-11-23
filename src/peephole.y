%{
#include <stdio.h>
#include <stdlib.h>

// Instruction types
#define TYPE_COMMENT 0
#define TYPE_INLINE_COMMENT 1
#define TYPE_DIRECTIVE 2
#define TYPE_LABEL 3
#define TYPE_CMD 4

typedef struct line {
    // Type:
    int type;
    char *name;
    int argc;
    char **argv;

    struct line *next;
} line;

void yyerror(char *error);
extern int yylex(void);
void add_line(int type, char *name, int argc, char **argv);
char **malloc_args(int argc);

line *first_line, *last_line;
int lineno = 0;

%}

%union {
    char *sval;
}

%token <sval> COMMENT DIRECTIVE LABEL WORD
%token NEWLINE COMMA COLON

%%

input:
    /* Empty */
    | input line
    ;

line:
    NEWLINE
    | COMMENT NEWLINE               { add_line(TYPE_COMMENT, $1, 0, NULL); }
    | instruction NEWLINE
    | instruction COMMENT NEWLINE   { add_line(TYPE_INLINE_COMMENT, $2, 0, NULL); }
    ;

instruction:
    command
    | DIRECTIVE                     { add_line(TYPE_DIRECTIVE, $1, 0, NULL); }
    | WORD COLON                    { add_line(TYPE_LABEL, $1, 0, NULL); }
    | error
    ;

command:
    WORD WORD COMMA WORD COMMA WORD {
            char **argv = malloc_args(3);
            argv[0] = $2;
            argv[1] = $4;
            argv[2] = $6;
            add_line(TYPE_CMD, $1, 3, argv);
        }
    | WORD WORD COMMA WORD {
            char **argv = malloc_args(2);
            argv[0] = $2;
            argv[1] = $4;
            add_line(TYPE_CMD, $1, 2, argv);
        }
    | WORD WORD {
            char **argv = malloc_args(1);
            argv[0] = $2;
            add_line(TYPE_CMD, $1, 1, argv);
        }
    ;

%%

extern int yylex();
extern int yyparse();
extern FILE *yyin;

/*int main(void) {
    return yyparse();
}*/

int main(int argc, const char *argv[]) {
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

void yyerror(char *error) {
    fprintf(stderr, "Error at line %d: %s\n", lineno, error);
}

void add_line(int type, char *name, int argc, char **argv) {
    line *l = (line*)malloc(sizeof(line));
    printf("%d: %s\n", lineno, name);

    l->argc = argc;
    l->argv = argv;

    if( last_line == NULL ) {
        // First line
        first_line = last_line = l;
    } else {
        // Add line to linked list
        last_line = last_line->next = l;
    }
}

char **malloc_args(int argc) {
    return (char **)malloc(3 * sizeof(char *));
}
