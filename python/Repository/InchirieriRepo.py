from Domain.Validators import *
from Repository.ClientRepo import *
from Repository.CartiRepo import *

class Inchirieri:

    def __init__(self):
        self.__inchiriere={}

    def adauga_inchirieri(self,id_client,id_carte):
        if id_client not in self.__inchiriere:
            self.__inchiriere[id_client] = []
        if id_carte not in self.__inchiriere[id_client]:
            self.__inchiriere[id_client].append(id_carte)

    def sterge_inchirieri(self,id_client,id_carte):
        if id_client in self.__inchiriere and id_carte in self.__inchiriere[id_client]:
            self.__inchiriere[id_client].remove(id_carte)
            if not self.__inchiriere[id_client]:  # Eliminăm clientul dacă nu mai are cărți închiriate
                del self.__inchiriere[id_client]
        else:
            raise ValueError("Inchirierea nu a fost găsită.")
        
    def get_inchirieri_client(self, id_client):
        """
        Returnează toate cărțile închiriate de un client.
        """
        return self.__inchiriere.get(id_client, [])

    def get_inchirieri_carte(self, id_carte):
        """
        Returnează toți clienții care au închiriat o anumită carte.
        """
        clienti = []
        for client, carti in self.__inchiriere.items():
            if id_carte in carti:
                clienti.append(client)
        return clienti

    def get_frecventa_clienti(self):
        """
        Returnează frecvența închirierilor pe client.
        """
        return {client: len(carti) for client, carti in self.__inchiriere.items()}
    
    def get_frecventa_carti(self):
        return {carte: len(clienti) for carte,clienti in self.__inchiriere.items()}

    def get_all(self):
        """
        Returnează toate închirierile.
        """
        return [(client, carte) for client, carti in self.__inchiriere.items() for carte in carti]