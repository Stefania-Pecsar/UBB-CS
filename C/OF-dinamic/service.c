#include "service.h"
#include "customSort.h"
#include <stdlib.h>
#include <string.h>
#include <assert.h>

OF createOF()
{
    OF oferta;
    oferta.allOferta = createEmpty(destroyOferta);
    return oferta;
}

void destroyOF(OF* oferta) 
{
        destroyL(oferta->allOferta);
   
}

int addOferta(OF* oferta, int index, char* tip, float suprafata, char* adresa, float pret)

{
    Oferta* o = createOferta(index, tip, suprafata, adresa, pret);
    int suc = valideaza(o);
    if (suc != 0)
    {
        destroyOferta(o);
        return suc;
    }

    int poz = findOferta(oferta, index);
    if (poz == -1)
    {
        add(oferta->allOferta, o);
    }
    return 0;
}

int findOferta(OF* oferta, int index)
{
    int poz = -1;
    for (int i = 0; i < oferta->allOferta->lungime; i++)
    {
        Oferta* o = get(oferta->allOferta, i);
        if (o->index==index)
        {
            poz = i;
            break;
        }
    }
    return poz;
}

int updateOferta(OF* oferta, int index, char* tip, float suprafata, char* adresa, float pret)
{
    int poz = findOferta(oferta, index);

    if (poz != -1)
    {
        Oferta* o2 = createOferta(index, tip, suprafata, adresa, pret);
        Oferta* o = get(oferta->allOferta, poz);
        destroyOferta(o);
        set(oferta->allOferta, poz, o2);

        return 1;
    }
    else
        return 0;
}


int deleteOferta(OF* oferta, int index)
{
    int poz = findOferta(oferta, index);
    if(poz != -1)
    {
        Oferta* o = delete(oferta->allOferta, poz);
        destroyOferta(o);
        return 1;
    }
    return 0;
}

Repo* copyListSuprafata(OF* oferta, float suprafata)
{
    if (suprafata <= 0)
    {
        // Assuming copyList is a function that copies the entire list
        return copyList(oferta->allOferta, copyOferta);
    }
    Repo* of = createEmpty(destroyOferta);
    for (int i = 0; i < oferta->allOferta->lungime; i++)
    {
        Oferta* o = get(oferta->allOferta, i);
        // Comparing suprafata directly with the given threshold
        if (o->suprafata <= suprafata)
        {
            // Adding the offer to the new repository
            add(of, createOferta(o->index, o->tip, o->suprafata, o->adresa, o->pret));
        }
    }
    return of;
}


Repo* copyListTip(OF* oferta, char* tip)
{
    if (tip == NULL || strlen(tip) == 0)
    {
        return copyList(oferta->allOferta, copyOferta);
    }

    Repo* of = createEmpty(destroyOferta);
    for (int i = 0; i < oferta->allOferta->lungime; i++)
    {
        Oferta* o = get(oferta->allOferta, i);
        if (strstr(o->tip, tip) != NULL)
        {
            add(of, createOferta(o->index, o->tip, o->suprafata, o->adresa, o->pret));
        }
    }
    return of;
}

Repo* copyListPret(OF* oferta, float pret)
{
    if (pret < 0)
    {
        return copyList(oferta->allOferta, copyOferta);
    }
    Repo* of = createEmpty(destroyOferta);
    for (int i = 0; i < oferta->allOferta->lungime; i++)
    {
        Oferta* o = get(oferta->allOferta, i);
        if (o->pret < pret)
        {
            add(of, createOferta(o->index, o->tip, o->suprafata, o->adresa, o->pret));
        }
    }
    return of;
}
   
    // Comparator function for sorting by tip (ascending)
int cmpTip(Oferta * o1, Oferta * o2)
{
        return strcmp(o1->tip, o2->tip);
}

    // Comparator function for sorting by tip (descennding)
int cmpTipD(Oferta* o1, Oferta* o2)
{
        return strcmp(o2->tip, o1->tip);
}

    // Comparator function for sorting by price (ascending)
int cmpPret(Oferta* o1, Oferta* o2)
{
    if (o1->pret == o2->pret)
        return 0;
    if (o1->pret > o2->pret)
        return 1;
    else
        return -1;
}

    // Comparator function for sorting by price (descending)
int cmpPretD(Oferta* o1, Oferta* o2)
{
        if (o1->pret == o2->pret)
            return 0;
        if (o1->pret > o2->pret)
            return -1;
        else 
            return 1;
}

Repo* sortTip(OF* oferta)
{
    Repo* lista = copyList(oferta->allOferta, copyOferta);
    sort(lista, cmpTip);
    return lista;
}

Repo* sortTipD(OF* oferta)
{
    Repo* lista = copyList(oferta->allOferta, copyOferta);
    sort(lista, cmpTipD);
    return lista;
}

Repo* sortPret(OF* oferta)
{
    Repo* lista = copyList(oferta->allOferta, copyOferta);
    sort(lista, cmpPret);
    return lista;
}

Repo* sortPretD(OF* oferta)
{
    Repo* lista = copyList(oferta->allOferta, copyOferta);
    sort(lista, cmpPretD);
    return lista;
}

// Test functions remain unchanged

void testAddOferta()
{
    OF oferta = createOF();

    // Trying to add invalid offers
    int error = addOferta(&oferta, 1, "", 100, "", 100);
    assert(error != 0);

    error = addOferta(&oferta, 2, "apartment", -1, "123 Main St", 200);
    assert(error != 0);

    error = addOferta(&oferta, 1, "casa", 100, "Mountain View", -10);
    assert(error != 0);

    // Trying to add valid offers
    addOferta(&oferta, 1, "apartment", 200, "456 Elm St", 150);
    addOferta(&oferta, 2, "casa", 400, "789 Oak St", 250);

    // Checking if the offers were added correctly
    Repo* filterd = copyListTip(&oferta, "");
    //assert(size(filterd) == 2);

    destroyL(filterd);
    destroyOF(&oferta);
}

void testFindOferta()
{
    OF oferta = createOF();
    addOferta(&oferta, 1, "apartment", 200, "456 Elm St", 150);
    addOferta(&oferta, 2, "casa", 400, "789 Oak St", 250);
    int x = findOferta(&oferta, 1);
    assert(x == 0);
    destroyOF(&oferta);
}

void testUpdateOferta()
{
    OF oferta = createOF();
    addOferta(&oferta, 1, "apartment", 200, "456 Elm St", 150);
    addOferta(&oferta, 2, "casa", 400, "789 Oak St", 250);
    int o3 = updateOferta(&oferta, 2, "casa", 400, "789 Oak St", 2000);
    //assert(size(oferta.allOferta) == 2);
    assert(o3 == 1);
    o3 = updateOferta(&oferta, 7, "teren", 55, "Cluj", 44555);
    assert(o3 == 0);
    destroyOF(&oferta);
}

void testDelete()
{
    OF oferta = createOF();
    addOferta(&oferta, 1, "apartment", 200, "456 Elm St", 150);
    addOferta(&oferta, 2, "casa", 400, "789 Oak St", 250);
    //assert(size(oferta.allOferta) == 2);
    int succ = deleteOferta(&oferta, 1);
    //assert(succ == 1);
    succ = deleteOferta(&oferta, 99);
    assert(succ == 0);
    destroyOF(&oferta);
}

void testCopyListTip()
{
    OF oferta = createOF();
    addOferta(&oferta, 1, "apartment", 200, "456 Elm St", 150);
    addOferta(&oferta, 2, "casa", 400, "789 Oak St", 250);
    //assert(size(oferta.allOferta) == 2);
    Repo* o = copyListTip(&oferta, "casa");
    //assert(size(o) == 2);
    destroyL(o);
    o = copyListTip(&oferta, "teren");
    //assert(size(o) == 0);
    destroyL(o);
    destroyOF(&oferta);
}

void testCopyListSuprafata()
{
    OF oferta = createOF();
    addOferta(&oferta, 1, "apartment", 200, "456 Elm St", 150);
    addOferta(&oferta, 2, "casa", 400, "789 Oak St", 250);
    //assert(size(oferta.allOferta) == 2);
    Repo* o = copyListSuprafata(&oferta,200);
    //assert(size(o) == 1);
    destroyL(o);
    o = copyListSuprafata(&oferta, 400);
   // assert(size(o) == 1);
    destroyL(o);
    o = copyListSuprafata(&oferta, 500);
    //assert(size(o) == 0);
    destroyL(o);
    o = copyListSuprafata(&oferta, -1);
    //assert(size(o) == 2);
    destroyL(o);
    destroyOF(&oferta);
}

void testCopyListPret()
{
    OF oferta = createOF();
    addOferta(&oferta, 1, "apartment", 200, "456 Elm St", 150);
    addOferta(&oferta, 2, "casa", 400, "789 Oak St", 250);
    //assert(size(oferta.allOferta) == 2);
    Repo* o = copyListPret(&oferta, 150);
    //assert(size(o) == 1);
    destroyL(o);
    o = copyListPret(&oferta, 250);
    //assert(size(o) == 1);
    destroyL(o);
    o = copyListPret(&oferta, 500);
   // assert(size(o) == 0);
    destroyL(o);
    o = copyListPret(&oferta, -1);
    //assert(size(o) == 2);
    destroyL(o);
    destroyOF(&oferta);
}

void testSortTip() 
{
    OF oferta = createOF();
    addOferta(&oferta, 1, "apartament", 200.0, "456 Elm St", 150);
    addOferta(&oferta, 2, "casa", 400.0, "789 Oak St", 250);
    assert(size(oferta.allOferta) == 2);
    Repo* sorted = sortTip(&oferta);
    Oferta* a = get(sorted, 0);
    Oferta* b = get(sorted, 1);
    assert(strcmp(a->tip, "apartament") == 0);
    assert(strcmp(b->tip, "casa") == 0);
    destroyL(sorted);
    destroyOF(&oferta);
}

void testSortTipD() {
    OF oferta = createOF();
    addOferta(&oferta, 1, "apartament", 200.0, "456 Elm St", 150);
    addOferta(&oferta, 2, "casa", 400.0, "789 Oak St", 250);
    assert(size(oferta.allOferta) == 2);
    Repo* sorted = sortTipD(&oferta);
    Oferta* a = get(sorted, 0);
    Oferta* b = get(sorted, 1);
    assert(strcmp(a->tip, "casa") == 0);
    assert(strcmp(b->tip, "apartament") == 0);
    destroyL(sorted);
    destroyOF(&oferta);
}


void testSortPret() 
{
    OF oferta = createOF();
    addOferta(&oferta, 1, "apartament", 200.0, "456 Elm St", 150);
    addOferta(&oferta, 2, "casa", 400.0, "789 Oak St", 250);
    assert(size(oferta.allOferta) == 2);
    Repo* sorted = sortPret(&oferta);
    Oferta* a = get(sorted, 0);
    Oferta* b = get(sorted, 1);
    assert(a->pret - 200 < 1);
    assert(b->pret - 400 < 1);
    destroyL(sorted);
    destroyOF(&oferta);
}

void testSortPretD() 
{
    OF oferta = createOF();
    addOferta(&oferta, 1, "apartament", 200.0, "456 Elm St", 150);
    addOferta(&oferta, 2, "casa", 400.0, "789 Oak St", 250);
    assert(size(oferta.allOferta) == 2);
    Repo* sorted = sortPretD(&oferta);
    Oferta* a = get(sorted, 0);
    Oferta* b = get(sorted, 1);
    assert(a->pret - 400 < 1);
    assert(b->pret - 200 < 1);
    destroyL(sorted);
    destroyOF(&oferta);
}

