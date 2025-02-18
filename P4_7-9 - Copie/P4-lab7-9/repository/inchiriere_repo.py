from domain.entities import *
from domain.validatori import *
from repository.client_repo import *
from repository.carte_repo import *

class Inchirieri_in_memorie:

    def __init__(self):
        self.__inchiriere=[]

    def adauga_inchirieri(self,id1,id2):
        self.__inchiriere.append((id1,id2))

    def sterge_inchirieri(self,id1,id2):
        index=0
        ok=True
        for index in range(len(self.__inchiriere)):
            if self.__inchiriere[index][0]==id1 and self.__inchiriere[index][1]==id2:
                self.__inchiriere.pop(index)
                ok=False
                break
        if ok:
            raise ValueError("Inchirierea nu a fost valida")

    def get_list(self):
        freq=[0]*100
        for id1,id2 in self.__inchiriere:
            freq[id1]+=1
        return freq

    def get_all_for_max(self):
        freq=[0]*100
        mx=0
        idm=0
        for id1,id2 in self.__inchiriere:
            freq[id2]+=1
            if freq[id2]>mx:
                mx=freq[id2]
                idm=id2
        lista=[]
        for id1,id2 in self.__inchiriere:
            if id2==idm:
                lista.append(id1)
        return lista

    def get_all_id1(self,id):
        carti=[]
        for id1,id2 in self.__inchiriere:
            if id1==id:
                carti.append(id2)
        return carti

    def get_all_id2(self,id):
        client=[]
        for id1,id2 in self.__inchiriere:
            if id2==id:
                client.append(id1)
        return client

    def get_all(self):
        return self.__inchiriere

def test_adauga_inchirieri():
    repo_carti=Carte_in_memorie()
    repo_client=Client_in_memorie()
    repo_rent=Inchirieri_in_memorie()
    client=Client(1,"Stefania Pecsar","6040806204989")
    carte=(1,"Harry Potter","o carte faina","SF")
    repo_client.adauga_client(client)
    repo_carti.adauga_carte(carte)

    repo_rent.adauga_inchirieri(1,1)

    repo_rent.get_all()==[(1,1)]

def test_sterge_inchirieri():
    repo_carte=Carte_in_memorie()
    repo_client=Client_in_memorie()
    repo_inchirieri=Inchirieri_in_memorie()
    client=Client(1,"Stefania Pecsar","6040806204989")
    carte=Carte(1,"Harry Potter","o carte faina","SF")
    repo_client.adauga_client(client)
    repo_carte.adauga_carte(carte)

    repo_inchirieri.adauga_inchirieri(1,1)

    assert repo_inchirieri.get_all()==[(1,1)]

    repo_inchirieri.sterge_inchirieri(1,1)

    assert repo_inchirieri.get_all()==[]

def test_get_list():
    repo_inchirieri=Inchirieri_in_memorie()
    repo_inchirieri.adauga_inchirieri(1,2)
    repo_inchirieri.adauga_inchirieri(1,3)
    repo_inchirieri.adauga_inchirieri(2,4)
    repo_inchirieri.adauga_inchirieri(5,3)

    lst=repo_inchirieri.get_list()

    assert lst==[0,2,1,0,0,1]+[0]*94

def test_get_all_id1():
    repo_inchirieri=Inchirieri_in_memorie()
    repo_inchirieri.adauga_inchirieri(1,1)
    repo_inchirieri.adauga_inchirieri(1,2)
    assert repo_inchirieri.get_all_id1(1)==[1,2]

def test_last():
    repo_inchirieri=Inchirieri_in_memorie()
    repo_inchirieri.adauga_inchirieri(1,2)
    repo_inchirieri.adauga_inchirieri(1,3)
    repo_inchirieri.adauga_inchirieri(2,4)
    repo_inchirieri.adauga_inchirieri(5,3)

    lst=repo_inchirieri.get_all_for_max()

    assert lst==[1,5]



