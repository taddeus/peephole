%{
#include <stdio.h>
#include "y.tab.h"
%}

%%

[a-z0-9$._]+:       { yylval = yytext; return LABEL; }      /* Label */
\$[a-z0-9._]        { yylval = yytext; return ARG; }        /* Arg of instr */
^[a-z.]+            { yylval = yytext; return INSTR; }      /* Instruction */
\.[^\n]*            { yylval = yytext; return DIRECTIVE; }  /* Assembly */
\,                  { return COMMA; }                       /* Comma */
#[^\n]*             { yylval = yytext; return COMMENT; }    /* Comment */
\n                  { return NL; }                          /* New line */
	
[\s\t]+             { ; }                              /* Ignore whitespace */
