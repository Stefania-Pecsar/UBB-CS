from Domain.Entities import *
from Domain.Validators import *
from Repository.CartiRepo import *
import random
import string

class CarteService():
    
    def __init__(self,repo,validator):
        self.__repo=repo
        self.__validator=validator
        self.__books = []
        self.__index = 0

    def insert_carte(self, titlu, autor, descriere):
        if self.__repo.get_all_books() != []:
            list = self.__repo.get_all_books()
            id_list = list[-1].get_id()
            self.__index = int(id_list) + 1
        else:
            self.__index = self.__index + 1
        id = self.__index
        book=Carte(id,titlu,autor,descriere)
        self.__validator.validate(book)
        self.__repo.adauga_carte(book)
        return book

    def adauga_random_carti(self, numar):
        for _ in range(numar):
            random_id = random.randint(1, 100)
            random_titlu = ''.join(random.choice(string.ascii_letters) for _ in range(8))
            random_autor = ''.join(random.choice(string.ascii_letters) for _ in range(6))
            random_descriere = ''.join(random.choice(string.ascii_letters) for _ in range(20))

            carte_noua = Carte(
                id=random_id,
                titlu=random_titlu,
                autor=random_autor,
                descriere=random_descriere,
            )
            self.__repo.adauga_carte(carte_noua) 


    def afisare_carti(self):
        '''
        Afiseaza cartile
        :return: lista de carti
        :rtype: lista de obiecte
        '''
        return self.__repo.get_all()

    def erase_carte(self,id):
        self.__repo.sterge_carte(id)

    def modify_carte(self,id,titlu,descriere,autor):
        book=Carte(id,titlu,descriere,autor)
        self.__validator.validate(book)
        self.__repo.modifica_carte(id,titlu,descriere,autor)
        return book

    def search_by_id(self,id):
        book=self.__repo.cauta_carte_dupa_id(id)
        return book

    def search_by_param(self,descriere):
        book=self.__repo.cauta_carte_dupa_parametru(descriere)
        return book
   

    def search_id(self,id):
        self.__repo.cauta_id(id)

    def get_all(self):
        return self.__repo.get_all_books()
