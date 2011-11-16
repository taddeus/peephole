%{
#include <stdio.h>
#include "y.tab.h"
%}

%%

[a-z0-9$._]+:       { yylval.sval = yytext; return LABEL; }      /* Label */
\$[a-z0-9._]        { yylval.sval = yytext; return ARG; }        /* Arg of instr */
^[a-z.]+            { yylval.sval = yytext; return INSTR; }      /* Instruction */
\.[^\n]*            { yylval.sval = yytext; return DIRECTIVE; }  /* Assembly */
[,]                 { return COMMA; }                       /* Comma */
#[^\n]*             { yylval.sval = yytext; return COMMENT; }    /* Comment */
[\n]                { return NL; }                          /* New line */
	
[\s\t]+             { ; }                              /* Ignore whitespace */
