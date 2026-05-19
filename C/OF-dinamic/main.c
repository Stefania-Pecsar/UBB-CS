#define _CRTDBG_MAP_ALLOC
#include "oferte.h"
#include "repo.h"
#include "service.h"

#include <stdio.h>
#include <stdlib.h> // Pentru a folosi malloc și free
#include <crtdbg.h> 

#define ANSI_COLOR_RED     "\x1b[31m"
#define ANSI_COLOR_GREEN   "\x1b[32m"
#define ANSI_COLOR_YELLOW  "\x1b[33m"
#define ANSI_COLOR_BLUE    "\x1b[34m"
#define ANSI_COLOR_MAGENTA "\x1b[35m"
#define ANSI_COLOR_CYAN    "\x1b[36m"
#define ANSI_COLOR_RESET   "\x1b[0m"
/*
Creati o aplicatie care permite gestiunea ofertelor de la o agentie imobiliara.
Fiecare oferta are: tip (teren, casa, apartament), suprafata, adresa, pret

Aplicatia permite:
 a) Adaugarea de noi oferte.
 b) Actualizare oferte
 c) Stergere oferta
 d) Vizualizare oferete ordonat dupa pret, tip (crescator/descrescator)
 e) Vizualizare oferta filtorate dupa un criteriu (suprafata, tip, pret)
*/

void testAll()
{
    // Funcția de testare pentru toate componentele
    testCreateDestroy();
    testCreateLista();
    testIterateLista();
    testCopyLista();
    testAdd_validare();
    testAddOferta();
    testUpdateOferta();
    testDelete();
    testCopyListPret();
    testCopyListSuprafata();
    testCopyListTip();
    testSortTip();
    testSortTipD();
    testSortPret();
    testSortPretD();
    testDeleteOfertaLista();
    testUpdateLista();
}


void citesteOferta(OF* oferta)
{
    printf("Index: ");
    int index;
    scanf_s("%d", &index);
    printf("Tip: ");
    char tip[21];
    scanf_s("%s", tip, 21);
    printf("Suprafata: ");
    float suprafata;
    scanf_s("%f", &suprafata);
    printf("Adresa: ");
    char adresa[101];
    scanf_s("%s", adresa, 101);
    printf("Pret: ");
    float pret;
    scanf_s("%f", &pret);
    int error = addOferta(oferta, index, tip, suprafata, adresa, pret);
    if (error != 0) {
        printf(ANSI_COLOR_RED "\nOferta invalid.\n" ANSI_COLOR_RESET);
    }
    else {
        printf(ANSI_COLOR_GREEN "\nOferta adaugat.\n" ANSI_COLOR_RESET);
    }
}

void printAllOferta(Repo* lista)
{
    printf("\nOferte\n");

    for (int i = 0; i < size(lista); ++i) {
        Oferta* o = get(lista, i);
        printf("Index: %d  ", o->index);
        printf("Tip: %s  ", o->tip);
        printf("Suprafata: %.2f  ", o->suprafata);
        printf("Adresa : %s  ", o->adresa);
        printf("Pret: %.2f  \n", o->pret);
    }
    
}

void updateOfertaData(OF* oferta)
{
    printf("Index: ");
    int index;
    scanf_s("%d", &index);
    printf("Tip: ");
    char tip[21];
    scanf_s("%s", tip, 21);
    printf("Suprafata: ");
    float suprafata;
    scanf_s("%f", &suprafata);
    printf("Adresa: ");
    char adresa[101];
    scanf_s("%s", adresa, 101);
    printf("Pret nou: ");
    float pret;
    scanf_s("%f", &pret);

    int successful = updateOferta(oferta, index, tip, suprafata, adresa, pret);
    if (successful)
    {
        printf(ANSI_COLOR_GREEN "\nOferta modificata cu succes.\n" ANSI_COLOR_RESET);
    }
    else {
        printf(ANSI_COLOR_RED "\nNu exista oferta.\n" ANSI_COLOR_RESET);
    }
}

void deleteOfertaData(OF* oferta)
{
    printf("Introduceti indexul ofertei: ");
    int index;
    scanf_s("%d", &index);

    int error = deleteOferta(oferta, index);
    if (error)
        printf("Stergerea ofertei a fost efectuata!\n");
    else
        printf("Stergere neefectuata!\n");
}

void copyListT(OF* oferta)
{
    printf("Introduceti tip: ");
    char tip[21];
    scanf_s("%s", tip, 21);

    Repo* filteredT = copyListTip(oferta, tip);
    printAllOferta(filteredT);
}

void copyListS(OF* oferta)
{
    printf("Introduceti suprafata: ");
    float suprafata;
    scanf_s("%f", &suprafata);

    Repo* filteredS = copyListSuprafata(oferta, suprafata);
    printAllOferta(filteredS);
}

void copyListP(OF* oferta)
{
    printf("Introduceti pret: ");
    float pret;
    scanf_s("%f", &pret);

    Repo* filteredP = copyListSuprafata(oferta, pret);
    printAllOferta(filteredP);
}

void sortByTip(OF* oferta)
{
    Repo* lista = sortTip(oferta);
    printAllOferta(lista);
    destroyL(lista);
}

void sortByTipD(OF* oferta)
{
    Repo* lista = sortTipD(oferta);
    printAllOferta(lista);
    destroyL(lista);
}

void sortByPret(OF* oferta)
{
    Repo* lista = sortPret(oferta);
    printAllOferta(lista);
    destroyL(lista);
}

void sortByPretD(OF* oferta)
{
    Repo* lista = sortPretD(oferta);
    printAllOferta(lista);
    destroyL(lista);
}

void start()
{
    printf("-----OFERTE IMOBILIARE-----\n");
    OF oferta = createOF();
    int run = 1; 
    while (run)
    {
        printAllOferta(oferta.allOferta);
        printf(ANSI_COLOR_CYAN"\n1. Adauga oferta\n" ANSI_COLOR_RESET);
        printf(ANSI_COLOR_CYAN"2. Actualizare oferta\n" ANSI_COLOR_RESET);
        printf(ANSI_COLOR_CYAN"3. Sterge oferta\n" ANSI_COLOR_RESET);
        printf(ANSI_COLOR_CYAN"4. Sorteaza ofertele dupa pret \n" ANSI_COLOR_RESET);
        printf(ANSI_COLOR_CYAN"5. Sorteaza ofertele dupa pret descrescator \n" ANSI_COLOR_RESET);
        printf(ANSI_COLOR_CYAN"6. Sorteaza ofertele dupa tip \n" ANSI_COLOR_RESET);
        printf(ANSI_COLOR_CYAN"7. Sorteaza ofertele dupa tip descrescator \n" ANSI_COLOR_RESET);
        printf(ANSI_COLOR_CYAN"8. Filtreaza dupa tip \n" ANSI_COLOR_RESET);
        printf(ANSI_COLOR_CYAN"9. Filtreaza dupa suprafata \n" ANSI_COLOR_RESET);
        printf(ANSI_COLOR_CYAN"10. Filtreaza dupa pret \n" ANSI_COLOR_RESET);
        printf(ANSI_COLOR_RED"0. Exit\n "ANSI_COLOR_RESET);
        printf(ANSI_COLOR_MAGENTA "\nComanda:"ANSI_COLOR_RESET);
        int comanda = -1;
        scanf_s("%d", &comanda);
        printf("\n");
        switch (comanda)
        {
            case 1:
                citesteOferta(&oferta);
                break;
            case 2:
                updateOfertaData(&oferta);
                break;
            case 3:
                deleteOfertaData(&oferta);
                break;
            case 4:
                sortByPret(&oferta);
                break;
            case 5:
                sortByPretD(&oferta);
                break;
            case 6:
                sortByTip(&oferta);
                break;
            case 7:
                sortByTipD(&oferta);
                break;
            case 8:
                copyListT(&oferta);
                break;
            case 9:
                copyListS(&oferta);
                break;
            case 10:
                copyListP(&oferta);
                break;
            case 0:
                printf("La revedere!\n");
                run = 0;
                // Don't forget to free memory allocated for the repository
                destroyOF(&oferta);
                break;
            default:
                printf(ANSI_COLOR_RED"Comanda invalida!\n"ANSI_COLOR_RESET);
                break;
        }
    }

        
}

int main() 
{
    testAll();
    //start();
    return 0;
}

