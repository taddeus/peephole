%{
#include <stdio.h>
#include <stdlib.h>
void yyerror(char*);
%}

%union {
    int ival;
    char *sval;
}

%token NL COMMA
%token <ival> INT
%token <sval> COMMENT DIRECTIVE REG LABEL OFFSET INSTR REF

%%

symb:
    symb symb
    | COMMENT {printf("Found a comment: %s\n", $1);}
    | DIRECTIVE {printf("Found a directive: %s\n", $1);}
    | REG {printf("Found a registry address: %s\n", $1);}
    | LABEL {printf("Found a label: %s\n", $1);}
    | REF {printf("Found a label reference: %s\n", $1);}
    | INT {printf("Found an integer: %d\n", $1);}
    | INSTR {printf("Found an instruction: %s\n", $1);}
    | COMMA {printf("Found a comma\n");}
    | NL {printf("Found a newline\n");}
    ;
%%

extern int yylex();
extern int yyparse();
extern FILE *yyin;

main(int argc, const char* argv[])
{
    if (argc < 2)
    {
        printf("No file specified");
        exit(-1);
    }

    // open a file handle to a particular file:
	FILE *myfile = fopen(argv[1], "r");
	// make sure it is valid:
	if (!myfile) {
		printf("Cannot open %s\n", argv[1]);
		return -1;
	}
	// set lex to read from it instead of defaulting to STDIN:
	yyin = myfile;

	// parse through the input until there is no more:
	do {
		yyparse();
	} while (!feof(yyin));
}

void yyerror(char *s)
{
    printf("Found error: %s\n", s);
    exit(-1);
}
