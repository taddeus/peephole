%{
#include <stdio.h>
#include "y.tab.h"
%}

%%

[a-z0-9$._]+:       { return LABEL; }      /* Label */
\$[a-z0-9._]        { return ARG; }        /* Argument of instruction */
^[a-z.]+            { return INSTR; }      /* Instruction */
\.[^\n]*            { return DIRECTIVE; }  /* Assembly */
\,                  { return COMMA; }      /* Comma */
#[^\n]*             { return COMMENT; }    /* Comment */
\n                  { return NL; }         /* New line */
	
[\s\t]+    {;}
