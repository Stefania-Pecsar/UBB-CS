#include "oferte.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>


Oferta* createOferta(int index, char* tip, float suprafata, char* adresa, float pret)
{
    Oferta* of = malloc(sizeof(Oferta));
    if (of == NULL) 
    {
        return NULL;
    }

    int nrC = (int)strlen(tip) + 1;
    of->tip = malloc(nrC * sizeof(char));
    if (of->tip == NULL)
    {
        free(of);
        return NULL;
    }
    strcpy_s(of->tip,nrC, tip);
    

    nrC = (int)strlen(adresa) + 1;
    of->adresa = malloc(nrC * sizeof(char));
    if (of->adresa == NULL)
    {
        free(of->tip);
        free(of);
        return NULL;
    }
    strcpy_s(of->adresa, nrC, adresa);


    of->index = index;
    of->suprafata = suprafata;
    of->pret = pret;

    return of;
}

// Marcam oferta ca fiind distrusă și eliberăm memoria alocată dinamic pentru string-uri
void destroyOferta(Oferta* o) 
    {
    //o->index = -1;
    //o->tip[0] = '\0';
    //o->adresa[0]='\0';
    free(o->tip);
    free(o->adresa);
    //o->suprafata = -1;
    //o->pret = -1;
    free(o);
}

Oferta* copyOferta(Oferta*o)
{
    return createOferta(o->index, o->tip, o->suprafata, o->adresa, o->pret);
}

int valideaza(Oferta* o)
{
    if (strlen(o->tip)== 0 || ((strcmp(o->tip, "casa") != 0 && strcmp(o->tip, "teren") != 0 && strcmp(o->tip, "apartament") != 0)))
    {
        return 1;
    }
    if (o->suprafata < 0)
    {
        return 2;
    }
    if (strlen(o->adresa) == 0)
    {
        return 3;
    }
    if (o->pret <= 0)
    {
        return 4;
    }
    if (o->index < 0)
    {
        return 5;
    }
    return 0;
}

void testCreateDestroy()
{
    Oferta* o = createOferta(1, "casa", 120, "Str.Mihali", 1200);
    assert(o->index == 1);
    assert(strcmp(o->tip, "casa") == 0);
    assert(o->suprafata == 120);
    assert(strcmp(o->adresa, "Str.Mihali") == 0);
    assert(o->pret == 1200);

    destroyOferta(o);
    o = createOferta(1, "casa", 120, "Str.Mihali", 1200);
    //assert(valideaza(o) == 5);

    destroyOferta(o);
}
