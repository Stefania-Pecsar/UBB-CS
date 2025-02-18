import random

from termcolor import colored
from utils.utils import *

def cmp_name(elem):
    return elem[0]

def cmp_books(elem):
    return elem[1]

class console:
    def __init__(self,srv,srv1,srv2):
        self.__srv=srv
        self.__srv1=srv1
        self.__srv2=srv2

    #book zone
    def __add_book(self):
        nume=input("Introduceti numele cartii: ")
        autor=input("Introduceti autor: ")
        descriere=input("Introduceti descrierea: ")
        try:
            book=self.__srv.insert_carte(nume, autor, descriere)
            print(colored("Carte adaugata cu succes!","green"))
        except ValueError as ve:
            print(colored(ve,"red"))

    def __delete_book(self):
        try:
            id_m=int(input("Introduceti id-ul cartii de sters: "))
            self.__srv.erase_carte(id_m)
            print(colored("Cartea a fost stersa cu succes","green"))
        except ValueError as ve:
            print(colored(ve,"red"))

    def __modify_book(self):
        try:
            id_m=int(input("Introduceti id-ul cartii de sters: "))
            nume=input("Introduceti noul nume carte: ")
            autor=input("Introduceti noul autor al carii: ")
            descriere=input("Introduceti noua descriere a cartii: ")
            self.__srv.modify_carte(id_m,nume,autor,descriere)
            print(colored("Carte modificata cu succes","green"))
        except ValueError as ve:
            print(colored(ve,"red"))

    def __search_id_book(self):
        """
        Cauta o carte dupa id
        """
        try:
            id=int(input("Introduceti id-ul de cautare: "))
            carte=self.__srv.search_by_id(id)
            return carte
        except ValueError as ve:
            print(colored(ve,"red"))

    def __search_param_book(self):
        try:
            titlu=autor=descriere=""
            titlu=input("Introduceti titlul: ")
            autor=input("Introduceti autorul: ")
            descriere=input("Introduceti descrierea: ")
            carte=self.__srv.search_by_param(titlu,autor,descriere)
            return carte
        except ValueError as ve:
            print(colored(ve,"red"))

    def __random_carte(self):
        try:
            number = random.randint(1, 10)
            self.__srv2.adauga_random_carti(number)
            st = "Au fost adăugați " + str(number) + " carți"
            print(colored(st, "green"))
        except ValueError as ve:
            print(colored("Operatiunea a esuat", "red"))
        carti_adaugate = self.__srv2.get_all()
        print("Clienti adaugati:")
        for carti in carti_adaugate:
            print(carti)

    #client zone
    def __add_client(self):
        nume=input("Introduceti numele: ")
        CNP=input("Introduceti CNP-ul: ")
        try:
            self.__srv1.insert_client(nume, CNP)
            print(colored("Client adaugat cu succes!","green"))
        except ValueError as ve:
            print(colored(ve,"red"))

    def __delete_client(self):
        try:
            id_m=int(input("Introduceti id-ul clientului de sters: "))
            self.__srv1.erase_client(id_m)
            print(colored("Clientul a fost sters cu succes","green"))
        except ValueError as ve:
            print(colored(ve,"red"))

    def __modify_client(self):
        try:
            id_m=int(input("Introduceti id-ul clientului de modificat: "))
            name=input("Introduceti noul nume : ")
            CNP=input("Introduceti noul CNP: ")
            self.__srv1.modify_client(id_m,name,CNP)
            print(colored("Client modificat cu succes","green"))
        except ValueError as ve:
            print(colored(ve,"red"))

    def __search_id_client(self):
        try:
            id=int(input("Introduceti id-ul de cautare: "))
            customer=self.__srv1.search_by_id(id)
            return customer
        except ValueError as ve:
            print(colored(ve,"red"))

    def __search_param_client(self):
        try:
            name=CNP=""
            name=input("Introduceti numele: ")
            CNP=input("Introduceti CNP-ul: ")
            customer=self.__srv1.search_by_param(name,CNP)
            return customer
        except ValueError as ve:
            print(colored(ve,"red"))

    def __random_client(self):
        try:
            number = random.randint(1, 10)
            self.__srv1.adauga_random_clienti(number)
            st = "Au fost adăugați " + str(number) + " clienți"
            print(colored(st, "green"))
        except ValueError as ve:
            print(colored("Operatiunea a esuat", "red"))
        clienti_adaugati = self.__srv1.get_all()
        print("Clienti adaugati:")
        for client in clienti_adaugati:
            print(client)
    #rent zone

    def __rent(self):
        try:
            id1=int(input("Introduceti id-ul clientului: "))
            self.__srv1.search_id(id1)
            customer=self.__srv1.search_by_id(id1)
            print("Bine ai venit, "+str(customer.get_nume()))
            print("Acestea sunt cartiile disponibile:")
            for elem in self.__srv.get_all():
                print(elem)
            id2=int(input("Introduceti id-ul cartii: "))
            self.__srv.search_id(id2)
            self.__srv2.add_rent_op(id1,id2)
            print(colored("Cartea a fost inchiriata cu succes","green"))
        except ValueError as ve:
            print(colored(ve,"red"))

    def __return(self):
        try:
            id1=int(input("Introduceti id-ul clientului: "))
            self.__srv1.search_id(id1)
            customer=self.__srv1.search_by_id(id1)
            print("Bine ai venit, "+str(customer.get_nume()))
            print("Acestea sunt cartile inchiriate de dvs:")
            books=self.__srv2.get_all_for_id1(id1)
            for elem in books:
                book=self.__srv.search_by_id(elem)
                print(book)
            id2=int(input("Introduceti id-ul cartilor de returnat: "))
            self.__srv.search_id(id2)
            self.__srv2.remove_rent_op(id1,id2)
            print(colored("Cartea a fost returnat cu succes","green"))
        except ValueError as ve:
            print(colored(ve,"red"))

    #reports
    def __report_client_nr(self):
        client_list=[]
        customers_freq=self.__srv2.get_list_with_ids()
        for index in range(len(customers_freq)):
            if customers_freq[index]!=0:
                customer=self.__srv1.search_by_id(index)
                client_list.append([customer.get_nume(),customers_freq[index]])

        client_list.sort(key=cmp_name)
        for elem in client_list:
            print(colored("Nume","magenta"),end=" ")
            print(elem[0],end="  ")
            print(colored("carti inchiriate: ","magenta"),end="")
            print(elem[1])

    def __report_books_nr_recursiv(self, client_list, customer_freq, index):
        # functie recursiva care construieste lista de clienti cu carti inchiriate pentru raport, ordonata dupa nr de cari inchiriate
        if index<len(customer_freq):
            if customer_freq[index] != 0:
                customer = self.__srv1.search_by_id(index)
                client_list.append([customer.get_nume(), customer_freq[index]])

            self.__report_books_nr_recursiv(client_list, customer_freq, index + 1)

    def __report_books_nr(self):
        # afișează un raport al clienților cu carti închiriate, ordonat după numărul de cărți închiriate.
        client_list=[]
        customers_freq=self.__srv2.get_list_with_ids()
       # inițiază apelul recursiv pentru a construi lista de clienți
        self.__report_books_nr_recursiv(client_list, customers_freq, 0)

    # sortează lista de clienți după numărul de cărți închiriate
        client_list.sort(key=cmp_books)

        for elem in client_list:
            print(colored("Nume","magenta"),end=" ")
            print(elem[0],end="  ")
            print(colored("carti inchiriate: ","magenta"),end="")
            print(elem[1])
    
    def __report_books_top(self):
        client_list=[]
        customers_freq=self.__srv2.get_list_with_ids()

        for index in range(len(customers_freq)):
            if customers_freq[index]!=0:
                customer=self.__srv1.search_by_id(index)
                client_list.append([customer.get_nume(),customers_freq[index]])
        # Sortare după numărul de cărți închiriate
        insertion_sort(client_list,key=cmp_books,reverse=True)
        print("Raport stortat dupa numarul de carti inchiriate:")
        for elem in client_list:
            print(colored("Nume","magenta"),end=" ")
            print(elem[0],end="  ")
            print(colored("carti inchiriate: ","magenta"),end="")
            print(elem[1])
        # Sortare dupa nume
        insertion_sort(client_list,key=cmp_name,reverse=False)
        print("\nRaport sortat alfabetic dupa nume:")
        for elem in client_list:
            print(colored("Nume","magenta"),end=" ")
            print(elem[0],end="  ")
            print(colored("carti inchiriate: ","magenta"),end="")
            print(elem[1])
    
    def __report_books_20(self):
        client_list=[]
        customers_freq=self.__srv2.get_list_with_ids()
        for index in range(len(customers_freq)):
            if customers_freq[index]!=0:
                customer=self.__srv1.search_by_id(index)
                client_list.append([customer.get_nume(),customers_freq[index]])

        # Sortare dupa numarul de carti inchiriate
        comb_sort(client_list,key=cmp_books,reverse=True)
        print("Raport sortat dupa numarul de carti inchiriate:")
        for elem in client_list:
            print(colored("Nume","magenta"),end=" ")
            print(elem[0],end="  ")
            print(colored("carti inchiriate: ","magenta"),end="")
            print(elem[1])
            
        # Sortare după nume
        comb_sort(client_list, key=cmp_name, reverse=False)
        print("\nRaport sortat alfabetic după nume:")
        for elem in client_list:
            print(colored("Nume", "magenta"), end=" ")
            print(elem[0], end="  ")
            print(colored("carti inchiriate: ", "magenta"), end="")
            print(elem[1])

    def __report_recursiv(self, customer_list, customers_freq, index, top_percent, top_list):
    # funcție recursivă care generează un raport special pentru primii 10% clienți cu cele mai multe cărți închiriate.
        if index < len(customers_freq):
            if customers_freq[index] != 0:
            # obține informații despre client
                customer = customer_list.search_by_id(index)
            # adaugă în lista top_list
                top_list.append([customer.get_name(), customers_freq[index]])

        # apel recursiv pentru următorul element în listă
        self.__report_recursiv(customer_list, customers_freq, index + 1, top_percent, top_list)

    def __report_special(self):
        # genereaza si afiseaza un raport special pt primii 10% clienti cu cele mai multe cartiinchiriate
        customers = self.__srv2.get_list_with_id_max()
        customers_freq = self.__srv2.get_list_with_ids()

        client_list = []
        # inițiază apelul recursiv pentru a genera raportul
        self.__report_recursiv(self.__srv1, customers, customers_freq, 0, client_list)

         # sortează lista de top clienți după numărul de cărți închiriate
        client_list.sort(key=lambda x: x[1], reverse=True)
        # calculează numărul de clienți care alcătuiesc topul 10%
        top_10_percent = int(len(client_list) * 0.1)
        # selectează doar primii 10% clienți din lista sortată
        top_10_list = client_list[:top_10_percent]
        # sortează lista de top clienți după numărul de cărți închiriate și nume
        top_10_list.sort(key=lambda x: (x[1], x[0]))

        for elem in top_10_list:
            print(colored("Nume", "magenta"), end=" ")
            print(elem[0], end="  ")
            print(colored("carti inchiriate: ", "magenta"), end="")
            print(elem[1])



    def main(self):
        end=False
        while not(end):
            print(colored("Comenzi disponbibile","cyan")+": carte_noua, client_nou, sterge_carte, sterge_client, modifica_carte, modifica_client, exit")
            print("cauta_carte, cauta_client, inchiriaza_carte, returneaza_carte")
            print(colored("Comenzi rapoarte: ","cyan"))
            print("1.Raport clienți cu carti închiriate ordonat dupa nume = raport_carti_nume")
            print("2.Raport clienți cu carti închiriate ordonat dupa numărul de carti închiriate = raport_carti_nr")
            print("3.Raport cele mai închiriate carti = raport_top_carti")
            print("4.Raport primii 20% clienți cu cele mai multe carti = raport_20")
            print("5.Raport primele 10% cel mai putin inchiriate carti,dupa numele autorului = raport_special")
            command=input("Comanda este: ")
            command.lower().strip()
            if command=="carte_noua":
                self.__add_book()
            elif command=="sterge_carte":
                self.__delete_book()
            elif command=="modifica_carte":
                self.__modify_book()
            elif command=="client_nou":
                self.__add_client()
            elif command=="sterge_client":
                self.__delete_client()
            elif command=="modifica_client":
                self.__modify_client()
            elif command=="cauta_carte":
                print("Comenzi disponibile cautare: id, descriere")
                secondary_command=input("Introduceti comanada: ")
                if secondary_command=="id":
                    book=self.__search_id_book()
                    if book:
                        print(book)
                elif secondary_command=="descriere":
                    book=self.__search_param_book()
                    if book:
                        print(book)
                else:
                    print(colored("Comanda invalida", "red"))
            elif command=="cauta_client":
                print("Comenzi disponibile cautare: id, descriere")
                secondary_command=input("Introduceti comanada: ")
                if secondary_command=="id":
                    customer=self.__search_id_client()
                    if customer:
                        print(customer)
                elif secondary_command=="descriere":
                    customer=self.__search_param_client()
                    if customer:
                        print(customer)
                else:
                    print(colored("Comanda invalida", "red"))
            elif command=="inchiriaza_carte":
                self.__rent()
            elif command=="returneaza_carte":
                self.__return()
            elif command=="clienti_random":
                self.__random_client()
            elif command=="carti_random":
                self.__random_carte()
            elif command=="raport_carti_nume":
                self.__report_client_nr()
            elif command=="raport_carti_nr":
                self.__report_books_nr()
            elif command=="raport_top_carti":
                self.__report_books_top()
            elif command=="raport_20":
                self.__report_books_20()
            elif command=="raport_special":
                self.__report_special()
            elif command=="exit":
                end=True
            else:
                print(colored("Comanda invalida","red"))