%{
#include <stdio.h>
#include "y.tab.h"
%}
word    [a-zA-Z0-9$_]+
int     [0-9]+
%%

[\n]                { return NL; }                              /* Newline */
#.*                 { yylval.sval = yytext; return COMMENT; }   /* Comment */
\..*                { yylval.sval = yytext; return DIRECTIVE; } /* Assembly directive */
{word}:             { yylval.sval = yytext; return LABEL; }      /* Label */
{int}               { yylval.ival = atoi(yytext); return INT; } /* Integer */
{word}              { yylval.sval = yytext; return WORD; }      /* Label reference / registry address */
{int}(\({word}\))?  { yylval.sval = yytext; return OFFSET; }    /* Registry offset address */
[a-z0-9\.]+         { yylval.sval = yytext; return CMD;   }     /* Command */
[,]                 { return COMMA; }                           /* Comma */

[ \t]+              ;                                           /* Ignore whitespace */
