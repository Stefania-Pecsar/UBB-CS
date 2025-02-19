#ifndef REPO_H_
#define REPO_H_
#include <stdlib.h>
#include <crtdbg.h>
#define _CRTDBG_MAP_ALLOC
#include "oferte.h"

typedef void* ElemType;
typedef void (*DestroyFct)(ElemType);
typedef ElemType(*CopyFct)(ElemType);

typedef struct {
	ElemType* elemente; // Folosim pointer la tipul ElemType
	int capacitate; // Adaugam un câmp pentru capacitatea listei
	int lungime;
	DestroyFct dfnc;
} Repo;

/*
* Creearea unei liste vide
*/
Repo* createEmpty(DestroyFct f);

/*
* Distrugem lista
*/
void destroyL(Repo* lista);

/*
* Luam pe rand elementele din lista
* poz - pozitia elementului, trebuie sa fie valida
* returneaza elementul de pe pozitia data
*/
ElemType get(Repo* lista, int poz);

/* Setare element. */
ElemType set(Repo* lista, int poz, ElemType ele);
/*
* returneaza numarul de elemente din lista
*/
int size(Repo* lista);

//int add_validare(Repo* lista, ElemType element);

/*
* Adauga un element in lista
* post: elementul este adaugat la sfarsitul listei
*/
void add(Repo* lista, ElemType element);

void update(Repo* lista, ElemType element);

ElemType delete(Repo* lista, int index);

/*
* Facem o copie listei
* returneaza Repo care contine aceleasi elemente ca si lista
*/
Repo* copyList(Repo* lista, CopyFct copyfct);

void testCreateLista();
void testIterateLista();
void testAdd_validare();
void testDeleteOfertaLista();
void testUpdateLista();
void testCopyLista();

#endif /* REPO_H_ */

