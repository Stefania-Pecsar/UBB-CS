#include "repo.h"

#include <string.h>
#include <stdlib.h> // Pentru funcția malloc
#include <assert.h>

Repo* createEmpty(DestroyFct f) 
{
    Repo* of = malloc(sizeof(Repo));
    if (of == NULL) {
        // Tratarea erorii de alocare a memoriei
        return NULL;
    }
    of->capacitate = 1;
    of->lungime = 0;
    of->elemente = malloc(sizeof(ElemType) * of->capacitate);
    of->dfnc = f;
    return of;
}

void destroyL(Repo* lista) 
{
    for (int i = 0; i < size(lista); i++) 
    {
        lista->dfnc(lista->elemente[i]);
    }
    free(lista->elemente); // Eliberăm memoria alocată pentru lista de elemente
    free(lista);
}

ElemType get(Repo* lista, int poz)
{
    return lista->elemente[poz];
}

ElemType set(Repo* lista, int poz, ElemType ele) 
{
    ElemType replacedElement = lista->elemente[poz];
    lista->elemente[poz] = ele;
    return replacedElement;
}

int size(Repo* lista) 
{
    return lista->lungime;
}


void add(Repo* lista, ElemType ele) {
    if (lista->lungime >= lista->capacitate) {
        int newCap = lista->capacitate * 2;
        ElemType* aux_elems = malloc(sizeof(ElemType) * newCap);
        for (int i = 0; i < lista->lungime; i++) {
            aux_elems[i] = lista->elemente[i];
        }
        free(lista->elemente);
        lista->elemente = aux_elems;
        lista->capacitate = newCap;
    }
    lista->elemente[lista->lungime] = ele;
    lista->lungime++;
}

void update(Repo* lista, Oferta* element) {
    for (int i = 0; i < lista->lungime; ++i) {
        Oferta* o = get(lista, i);
        if (o->index == element->index) {
            o->pret = element->pret;
            return; 
        }
    }
}


ElemType delete(Repo* lista, int index)
{
    ElemType ele = lista->elemente[index-1];
    for (int i = index-1; i < lista->lungime - 1; i++) {
        lista->elemente[i] = lista->elemente[i + 1];
    }
    lista->lungime--;
    return ele;
}

Repo* copyList(Repo* lista,CopyFct copyFct) 
{
    Repo* of = createEmpty(lista->dfnc);
    for (int i = 0; i < size(lista); ++i) 
    {
        ElemType o = get(lista, i);
        add(of, copyFct(o));
    }
    return of;
}

void testCreateLista()
{
    Repo* lista = createEmpty(destroyOferta);
    assert(size(lista) == 0);
    destroyL(lista);
}

void testIterateLista() 
{
    Repo* lista = createEmpty(destroyOferta);
    add(lista,createOferta(1, "casa", 120, "Str.Mihali", 1200));
    add(lista, createOferta(2, "teren", 1500, "Str.Mihali", 14000));
    assert(size(lista) == 2);
    Oferta* o = get(lista, 0);
    assert(strcmp(o->tip, "casa") == 0);
    o = get(lista, 1);
    //assert(o->suprafata == 120);
    destroyL(lista);
    //assert(size(lista) == 0);
}

void testAdd_validare() 
{
    Repo* lista = createEmpty(destroyOferta);
    add(lista, createOferta(1, "casa", 120, "Str.Mihali", 1200));
    add(lista, createOferta(2, "teren", 1500, "Str.Mihali", 14000));
    assert(size(lista) == 2);
    add(lista, createOferta(1, "casa", 120, "Str.Mihali", 1200));
    //assert(size(lista) == 2);
    Oferta* o = get(lista, 0);
    assert(o->suprafata == 120);
}

void testUpdateLista() 
{
    Repo* lista = createEmpty(destroyOferta);
    add(lista, createOferta(1, "casa", 120, "Str.Mihali", 1200));
    add(lista, createOferta(2, "teren", 1500, "Str.Mihali", 14000));
    assert(size(lista) == 2);
    update(lista, createOferta(1, "casa", 120, "Str.Mihali", 1000));
    Oferta* o = get(lista, 0);
    assert(o->pret - 1000 < 1);
    assert(strcmp(o->tip, "casa") == 0);
    assert(o->suprafata - 120 < 1);
    assert(strcmp(o->adresa,"Str.Mihali") == 0);
}


void testDeleteOfertaLista() 
{
    Repo* lista = createEmpty(destroyOferta);
    add(lista, createOferta(1, "casa", 120, "Str.Mihali", 1200));
    add(lista, createOferta(2, "teren", 1500, "Str.Mihali", 14000));
    assert(size(lista) == 2);
    delete(lista, 1);
    assert(size(lista) == 1);
    Oferta* o = get(lista, 0);
    assert(strcmp(o->tip, "teren") == 0);
    assert(o->suprafata == 1500);
    assert(strcmp(o->adresa, "Str.Mihali") == 0);
    assert(o->pret == 14000);
}

void testCopyLista()
{
    Repo* lista = createEmpty(destroyOferta);
    add(lista, createOferta(1, "casa", 120, "Str.Mihali", 1200));
    add(lista, createOferta(2, "teren", 1500, "Str.Mihali", 14000));
    Repo* lista2 = copyList(lista,copyOferta);
    assert(size(lista2) == 2);
    Oferta* o = get(lista2, 0);
    assert(strcmp(o->tip, "casa") == 0);
    destroyL(lista);
    destroyL(lista2);
}


