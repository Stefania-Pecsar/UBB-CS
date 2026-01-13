%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "lab.tab.h"
int cuvinte_total = 0;
%}

%%

[a-z]+ {
yylval.cuvant = strdup(yytext);
cuvinte_total++;
return CUVENT;
}

[ \t\n\r]+ ; // Ignor spatii albe
. ; // Ignora alte carac

%%

int yywrap() {
return 1;
}