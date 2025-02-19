#ifndef SERVICE_H_
#define SERVICE_H_
#define _CRTDBG_MAP_ALLOC
#include <stdlib.h>
#include <crtdbg.h>
#include "repo.h"

typedef struct {
	Repo* allOferta;
}OF;

OF createOF();

void destroyOF(OF* oferta);

int addOferta(OF* oferta, int index, char* tip, float suprafata, char* adresa, float pret);

int deleteOferta(OF* oferta, int index);

int findOferta(OF* oferta, int index);

int updateOferta(OF* oferta, int index, char* tip, float suprafata, char* adresa, float pret);

Repo* copyListTip(OF* oferta, char* tip);

Repo* copyListSuprafata(OF* oferta, float suprafata);

Repo* copyListPret(OF* oferta, float pret);

/*
Repo* cmpTip(Oferta* o1, Oferta* o2);
Repo* cmpTipD(Oferta* o1, Oferta* o2);
Repo* cmpPretD(Oferta* o1, Oferta* o2);
Repo* cmpPretD(Oferta* o1, Oferta* o2);
*/

Repo* sortTip(OF* oferta);
Repo* sortPret(OF* oferta);
Repo* sortTipD(OF* oferta);
Repo* sortPretD(OF* oferta);

void testAddOferta();
void testFindOferta();
void testUpdateOferta();
void testDelete();
void testCopyListTip();
void testCopyListSuprafata();
void testCopyListPret();
void testSortTip();
void testSortTipD();
void testSortPret();
void testSortPretD();
#endif // SERVICE_H_