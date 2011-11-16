%{
#include <stdio.h>
#include "y.tab.h"
%}
reg     \$[a-zA-Z0-9]+
label   [a-zA-Z0-9_\.]+
int     [0-9]+
%%

[\n]                { return NL; }                              /* Newline */
#.*                 { yylval.sval = yytext; return COMMENT; }   /* Comment */
\..*                { yylval.sval = yytext; return DIRECTIVE; } /* Assembly directive */
{label}:            { yylval.sval = yytext; return LABEL; }     /* Label */
{reg}               { yylval.sval = yytext; return REG; }       /* Registry address */
{int}               { yylval.ival = atoi(yytext); return INT; } /* Integer */
{int}(\({reg}\))?   { yylval.sval = yytext; return OFFSET; }    /* Registry offset */
[a-z0-9\.]+         { yylval.sval = yytext; return INSTR; }     /* Instruction */
{label}             { yylval.sval = yytext; return REF; }       /* Label reference */
[,]                 { return COMMA; }                           /* Comma */

[ \t]+              ;                                           /* Ignore whitespace */
