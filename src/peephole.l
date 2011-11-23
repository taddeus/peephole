%{
#include <stdio.h>
#include <string.h>
#include "y.tab.h"

extern int lineno;
%}

%option noyywrap

word    [a-zA-Z0-9$_.]+
int     [0-9]+

%%

\n                  { lineno++; printf("ikmatchhemwel!"); return NEWLINE; }
:                   { return COLON; }
,                   { return COMMA; }
#.*                 { yylval.sval = strdup(yytext); return COMMENT; }
\..*                { yylval.sval = strdup(yytext); return DIRECTIVE; }
{word}              { yylval.sval = strdup(yytext); return WORD; }
{int}(\({word}\))?  { yylval.sval = strdup(yytext); return WORD; }

[ \t]+              ;
