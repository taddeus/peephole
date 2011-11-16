%{
#include <stdio.h>
#include <stdlib.h>
void yyerror(char*);
%}

%token COMMA NL

%union {
    char *sval;
}

%token <sval> LABEL
%token <sval> ARG
%token <sval> INSTR
%token <sval> DIRECTIVE
%token <sval> COMMENT

%%
symb:
    LABEL {printf("Found a label: %s\n", $1);}
    | ARG {printf("Found an argument: %s\n", $1);}
    | INSTR {printf("Found an instruction: %s\n", $1);}
    | DIRECTIVE {printf("Found a directive: %s\n", $1);}
    | COMMA {printf("Found a comma\n");}
    | COMMENT {printf("Found a comment: %s\n", $1);}
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
