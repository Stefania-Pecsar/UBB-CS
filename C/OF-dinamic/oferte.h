#ifndef OFERTE_H_
#define OFERTE_H_

typedef struct
{
	int index;
	char* tip; // pointer către un string pentru tip
	float suprafata;
	char* adresa; // pointer către un string pentru adresa
	float pret;
} Oferta;

/*
* Creearea unei noi oferte
*/

Oferta* createOferta(int index, char* tip, float suprafata, char* adresa, float pret);

/*
Copie oferta
*/

Oferta* copyOferta(Oferta*);

void destroyOferta(Oferta* o);

void testCreateDestroy();

int valideaza(Oferta* o);

#endif /* OFERTE_H_ */
