%{
#include <stdio.h>
#include "y.tab.h"
%}
reg     \$[a-zA-Z0-9]+
word    [a-zA-Z0-9_\.]+
int     [0-9]+
%%

[\n]                { return NL; }                              /* Newline */
#.*                 { yylval.sval = yytext; return COMMENT; }   /* Comment */
\..*                { yylval.sval = yytext; return DIRECTIVE; } /* Assembly directive */
{word}:             { yylval.sval = yytext; return LABEL; }     /* Label */
{reg}               { yylval.sval = yytext; return REG; }       /* Registry address */
{int}               { yylval.ival = atoi(yytext); return INT; } /* Integer */
{int}(\({reg}\))?   { yylval.sval = yytext; return OFFSET; }    /* Registry offset */
[a-z\.]+            { yylval.sval = yytext; return INSTR; }     /* Instruction */
{word}              { yylval.sval = yytext; return REF; }       /* Label reference */
[,]                 { return COMMA; }                           /* Comma */

[ \t]+              ;                                           /* Ignore whitespace */
