%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
char *cuvant;
int count;
} CuvantCount;

CuvantCount *cuvinte_derivate = NULL;
int num_cuvinte_derivate = 0;
int capacitate_derivate = 0;

void adauga_cuvant_derivat(const char *cuvant);
int este_derivat(const char *cuvant);
void afiseaza_rezultate();
void elibereaza_memoria();

extern int cuvinte_total;
extern void yyerror( char *s);
int yylex();
%}

%union {
char *cuvant;
}

%token <cuvant> CUVENT

%%

text:
| text CUVENT {
if (este_derivat($2)) {
adauga_cuvant_derivat($2);
}
free($2);
}
;

%%

int este_derivat(const char *cuvant) {
// Verific daca cuv cont rad "ceremoni"
return strstr(cuvant, "ceremoni") != NULL;
}

void adauga_cuvant_derivat(const char *cuvant) {
// Caut daca cuv e deja
for (int i = 0; i < num_cuvinte_derivate; i++) {
if (strcmp(cuvinte_derivate[i].cuvant, cuvant) == 0) {
cuvinte_derivate[i].count++;
return;}
}
if (num_cuvinte_derivate >= capacitate_derivate) {
    capacitate_derivate = capacitate_derivate == 0 ? 10 : capacitate_derivate * 2;
    cuvinte_derivate = realloc(cuvinte_derivate, capacitate_derivate * sizeof(CuvantCount));
}

cuvinte_derivate[num_cuvinte_derivate].cuvant = strdup(cuvant);
cuvinte_derivate[num_cuvinte_derivate].count = 1;
num_cuvinte_derivate++;
}

void afiseaza_rezultate() {
printf("Numar total de cuvinte: %d\n", cuvinte_total);
printf("\nCuvinte derivate din 'ceremonie':\n");

if (num_cuvinte_derivate == 0) {
    printf("Nu s-au gasit cuvinte derivate.\n");
} else {
    for (int i = 0; i < num_cuvinte_derivate; i++) {
        printf("%s: %d aparitii\n", cuvinte_derivate[i].cuvant, cuvinte_derivate[i].count);
    }
}
}

void elibereaza_memoria() {
for (int i = 0; i < num_cuvinte_derivate; i++) {
free(cuvinte_derivate[i].cuvant);
}
free(cuvinte_derivate);
}

int main(int argc, char *argv[]) {
extern FILE *yyin;

if (argc > 1) {
    yyin = fopen(argv[1], "r");
    if (!yyin) {
        fprintf(stderr, "Eroare: Nu pot deschide fisierul %s\n", argv[1]);
        return 1;
    }
} else {
    yyin = stdin;
    printf("Introduceti textul (Ctrl+D pentru a termina):\n");
}

yyparse();

afiseaza_rezultate();
elibereaza_memoria();

if (argc > 1) {
    fclose(yyin);
}

return 0;
}

void yyerror( char *s) {
fprintf(stderr, "Eroare: %s\n", s);
exit(1);
}