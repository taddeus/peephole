%{
#include <stdio.h>
#include "y.tab.h"
%}
arg \$[a-zA-Z0-9\.]+

%%

#[^\n]*             { yylval.sval = yytext; return COMMENT; }    /* Comment */
[a-zA-Z0-9$\.]+:   { yylval.sval = yytext; return LABEL; }      /* Label */
{arg}               { yylval.sval = yytext; return ARG; }        /* Arg of instr */
[0-9]+(\({arg}\))?  { yylval.sval = yytext; return ARG; }        /* Arg of instr */
\.[^\n]*            { yylval.sval = yytext; return DIRECTIVE; }  /* Assembly */
[a-z\.]+            { yylval.sval = yytext; return INSTR; }      /* Instruction */
[,]                 { return COMMA; }                       /* Comma */
[\n]                { return NL; }                          /* New line */
	
[ \t]+             { ; }                            /* Ignore whitespace */
