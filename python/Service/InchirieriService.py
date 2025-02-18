from Domain.Entities import *
from Domain.Validators import *
from Repository.InchirieriRepo import *
from utils.utils import *

def cmp_name(elem):
    return elem[0]

def cmp_books(elem):
    return elem[1]

class RentService():
    def __init__(self,repo):
        self.__repo=repo

    def add_rent_op(self, id1, id2):
        if id1 < 0 or id2 < 0:
            raise ValueError("ID-urile trebuie să fie pozitive.")
        self.__repo.adauga_inchirieri(id1, id2)

    def afisare(self):
        '''
        Returneaza lista de inchirieri
        :return: lista de inchirieri
        '''
        return self.__repo.get_all()

    def remove_rent_op(self,id1,id2):
        self.__repo.sterge_inchirieri(id1,id2)
    
    def test_get_list(self):
        lst=self.__rent_srv.get_list_with_ids()

    def get_list_with_ids(self):
        return self.__repo.get_list()

    def get_list_with_id_max(self):
        return self.__repo.get_all_for_max()

    def get_all_for_id1(self,id):
        return self.__repo.get_all_id1(id)

    def get_all_for_id2(self,id):
        return self.__repo.get_all_id2(id)
    
    def get_all_rentals(self):
        return self.__repo.get_all()
    
    def report_books_20(self):
        client_list = []
        customers_freq = self.__srv2.get_list_with_ids()

        for index in range(len(customers_freq)):
            if customers_freq[index] != 0:
                customer = self.__srv1.search_by_id(index)
                client_list.append([customer.get_nume(), customers_freq[index]])

        # Sortare după numărul de cărți închiriate folosind Gnome Sort
        gnome_sort(client_list, key=cmp_books, reverse=True)
        print("Raport sortat dupa numarul de carti inchiriate:")
        for elem in client_list:
            print(colored("Nume", "magenta"), end=" ")
            print(elem[0], end="  ")
            print(colored("carti inchiriate: ", "magenta"), end="")
            print(elem[1])

        # Sortare după nume folosind Gnome Sort
        gnome_sort(client_list, key=cmp_name, reverse=False)
        print("\nRaport sortat alfabetic după nume:")
        for elem in client_list:
            print(colored("Nume", "magenta"), end=" ")
            print(elem[0], end="  ")
            print(colored("carti inchiriate: ", "magenta"), end="")
            print(elem[1])


    def report_top_20_books(self):
        books_list = []
        books_freq = self.__rental_service.get_list_with_ids()

        for index in range(len(books_freq)):
            if books_freq[index] != 0:
                book = self.__book_service.search_book_by_id(index)
                books_list.append([book.get_titlu(), books_freq[index]])

        # Sortare cu Quick Sort
        books_list = quick_sort(books_list, key=lambda x: x[1], cmp=lambda x, y: x > y, reverse=True)

        # Determinăm primele 20% cărți
        top_count = len(books_list) * 2 // 10
        print(colored("Raport: Cele mai închiriate 20% cărți", "cyan"))
        for i in range(top_count):
            print(colored("Titlu", "magenta"), end=" ")
            print(books_list[i][0], end="  ")
            print(colored("Număr de închirieri: ", "magenta"), end="")
            print(books_list[i][1])