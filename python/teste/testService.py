import unittest

from Domain.Entities import *
from Repository.CartiRepo import *
from Service.Carti_service import *
from Domain.Validators import *
from Repository.ClientRepo import *
from Service.Client_service import *
from Service.InchirieriService import *
from Repository.InchirieriRepo import *

class TestBookService(unittest.TestCase):
    def setUp(self) -> None:
        self.__test_valid=CartiValidator()
        self.__test_repo=CarteRepo()
        self.__test_srv=CarteService(self.__test_repo,self.__test_valid)

    def test_insert_carte(self):
        book=self.__test_srv.insert_carte(1,"Harry Potter","J.K.Rowling","o carte faina")
        self.assertEqual(book.get_id(),1)
        self.assertEqual(book.get_titlu(),"Harry Potter")
        self.assertEqual(book.get_autor(),"J.K.Rowling")
        self.assertEqual(book.get_descriere(),"o carte faina")

        self.assertRaises(ValueError,self.__test_srv.insert_carte,1,"","J.K.Rowling","o carte faina")

    def test_erase_carte(self):
        book1=self.__test_srv.insert_carte(1,"Harry Potter","J.K.Rowling","o carte faina")
        book2=self.__test_srv.insert_carte(2,"Pasarea Spin","Colleen McCullough","")

        self.__test_srv.erase_carte(2)
        self.assertEqual(len(self.__test_srv.get_all()),1)

        self.__test_srv.erase_bookf(1)
        self.assertEqual(len(self.__test_srv.get_all()),0)

    def test_modify_book(self):
        book1=self.__test_srv.insert_carte(1,"Harry Potter","J.K.Rowling","o carte faina")
        book2=self.__test_srv.insert_carte(2,"Pasarea Spin","Colleen McCullough")

        book1=self.__test_srv.modify_carte(1,"Razboiul celor 2 roze","Conn Iggulden","carte istorica")
        self.assertEqual(book1.get_id(),1)
        self.assertEqual(book1.get_titlu(),"Razboiul celor 2 roze")
        self.assertEqual(book1.get_autor(),"Conn Iggulden")
        self.assertEqual(book1.get_titlu(),"carte ostorica")
        self.assertRaises(ValueError,self.__test_srv.modify_carte,1,"","Conn Iggulden","carte istorica")

    def test_get_all(self):
        carte1=self.__test_srv.insert_carte(1,"Harry Potter","J.K.Rowling","o carte faina")
        carte2=self.__test_srv.insert_carte(2,"Pasarea Spin","Colleen McCullough","carte istorica")

        self.assertEqual(len(self.__test_srv.get_all()),2)

    def test_search_by_id(self):
        carte1=self.__test_srv.insert_carte(1,"Harry Potter","J.K.Rowling","o carte faina")
        carte2=self.__test_srv.insert_carte(2,"Pasarea Spin","Colleen McCullough")

        self.assertEqual(self.__test_srv.search_by_id(1),carte1)
        self.assertEqual(self.__test_srv.search_by_id(2),carte2)
        self.assertRaises(ValueError,self.__test_srv.search_by_id,3)

    def test_search_by_param(self):
        carte1=self.__test_srv.insert_carte(1,"Harry Potter","J.K.Rowling","o carte faina")
        carte2=self.__test_srv.insert_carte(2,"Pasarea Spin","Colleen McCullough")

        self.assertEqual(self.__test_srv.search_by_param("Harry Potter","",""),carte1)
        self.assertEqual(self.__test_srv.search_by_param("","J.K.Rowling","o carte faina"),carte2)
        self.assertRaises(ValueError,self.__test_srv.search_by_param,"","","")
        self.assertRaises(ValueError,self.__test_srv.search_by_param,"","J.K.Rowling","")

    def test_adauga_random_carti(self,random_choice, random_randint):
        random_randint.return_value = 42  
        random_choice.side_effect = lambda seq: seq[0]  

        repo = CarteRepo()
        repo.adauga_random_carti(5)

        self.assertEqual(len(repo._CarteRepo__index), 5)

        for carte in repo._CarteRepo__index:
            self.assertEqual(carte.id, 42) 
            self.assertEqual(carte.titlu, 'aaaaaaaa')  
            self.assertEqual(carte.autor, 'aaaaaa') 
            self.assertEqual(carte.descriere, 'aaaaaaaaaaaaaaaaaaaa') 

        self.assertEqual(CarteRepo.id, 6) 

class ClientServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.__test_repo=CarteRepo()
        self.__test_valid=ClientValidator()
        self.__test_srv=ClientService(self.__test_repo,self.__test_valid)

    def test_insert_client(self):
        customer=self.__test_srv.insert_client(1,"Stefania Pecsar","6040608204989")
        self.assertEqual(customer.get_id(),1)
        self.assertEqual(customer.get_nume(),"Stefania Pecsar")
        self.assertEqual(customer.get_cnp(),"6040806204989")

        self.assertRaises(ValueError,self.__test_srv.insert_client,1,"Stefania Pecsar","6040608204989")

    def test_erase_client(self):
        customer1=self.__test_srv.insert_client(1,"Stefania Pecsar","6040608204989")
        customer2=self.__test_srv.insert_client(2,"Stefania Morar","6040608204988")

        self.__test_srv.erase_client(2)
        self.assertEqual(len(self.__test_srv.get_all()),1)

    def test_modify_customer(self):
        customer1=self.__test_srv.insert_client(1,"Stefania Pecsar","6040608204989")
        customer2=self.__test_srv.insert_client(2,"Stefania Morar","6040608204988")

        mod_customer=self.__test_srv.modify_client(1,"Stefania Pecsar","6040608204989")
        self.assertEqual(mod_customer.get_id(),1)
        self.assertEqual(mod_customer.get_nume(),"Stefania Pecsar")
        self.assertEqual(mod_customer.get_cnp(),"6040806204989")

        self.assertRaises(ValueError,self.__test_srv.insert_client,2,"","6040806204989")

    def test_search_by_id(self):
        customer1=self.__test_srv.insert_client(1,"Stefania Pecsar","6040608204989")
        customer2=self.__test_srv.insert_client(2,"Stefania Morar","6040608204988")

        self.assertEqual(self.__test_srv.search_by_id(1),customer1)
        self.assertEqual(self.__test_srv.search_by_id(2),customer2)

        self.assertRaises(ValueError,self.__test_srv.search_by_id,3)

    def test_search_by_param(self):
        customer1=self.__test_srv.insert_client(1,"Stefania Pecsar","6040608204989")
        customer2=self.__test_srv.insert_client(2,"Stefania Morar","6040608204988")

        self.assertEqual(self.__test_srv.search_by_param("Stefania Pecsar",""),customer1)
        self.assertEqual(self.__test_srv.search_by_param("","6040806204989"),customer2)

        self.assertRaises(ValueError,self.__test_srv.search_by_param,"","")
        self.assertRaises(ValueError,self.__test_srv.search_by_param,"Stefi","")

    def test_get_all(self):
        customer1=self.__test_srv.insert_client(1,"Stefania Pecsar","6040608204989")
        customer2=self.__test_srv.insert_client(2,"Stefania Morar","6040608204988")

        self.assertEqual(len(self.__test_srv.get_all()),2)

    def test_adauga_random_clienti(self, random_choice):
        random_choice.side_effect = lambda seq: seq[0]  
        repo = ClientRepo()
        repo.adauga_random_clienti(3)
        self.assertEqual(len(repo._ClientRepo__clients), 3)
        for client in repo._ClientRepo__clients:
            self.assertEqual(client.id, 1)  
            self.assertEqual(client.nume, 'aaaaaaaa')  
            self.assertEqual(client.cnp, '0000000000000')  

        self.assertEqual(ClientRepo.id, 4)  

class RentServiceTest(unittest.TestCase):
    
    def setUp(self) -> None:
 
        self.__rent_repo = Inchirieri()
        self.__client_repo = ClientRepo()
        self.__book_repo = CarteRepo()

        self.__rent_validator = InchirieriValidator()


        self.__rent_srv = RentService(self.__rent_repo, self.__book_repo, self.__client_repo, self.__rent_validator)


        self.__client_repo.insert_client(Client(1, "Ion Popescu", "6040806204989"))
        self.__client_repo.insert_client(Client(2, "Maria Ionescu", "6040806204988"))
        self.__book_repo.insert_carte(Carte(1, "Harry Potter", "J.K. Rowling", "o carte faina"))
        self.__book_repo.insert_carte(Carte(2, "Cartea lui Ion", "Ion Popescu", "o altă carte faină"))

    def test_report_books_20(self):
        self.__rent_srv.add_rent_op(1, 1)  
        self.__rent_srv.add_rent_op(2, 1)  
        self.__rent_srv.add_rent_op(1, 2)  

        client_list = self.__rent_srv.get_list_with_ids()  
        self.assertEqual(client_list[0], 2)  
        self.assertEqual(client_list[1], 1)  

        self.__rent_srv.report_books_20()

       
        self.assertEqual(len(client_list), 2)
        
    def test_report_top_20_books(self):
        
        self.__rent_srv.add_rent_op(1, 1)  
        self.__rent_srv.add_rent_op(2, 1)  
        self.__rent_srv.add_rent_op(1, 2)  

        books_freq = self.__rent_srv.get_books_rental_frequency()
        self.assertEqual(books_freq[1], 2)  
        self.assertEqual(books_freq[2], 1)

        self.__rent_srv.report_top_20_books()


    def test_add_rent(self):
        self.__rent_srv.add_rent_op(1, 1)
        rentals = self.__rent_srv.get_all_rentals()
        self.assertEqual(len(rentals), 1)
        self.assertEqual(rentals[0].get_client_id(), 1)
        self.assertEqual(rentals[0].get_book_id(), 1)

    def test_remove_rent(self):
        self.__rent_srv.add_rent_op(1, 1)
        self.assertEqual(len(self.__rent_srv.get_all_rentals()), 1)
        self.__rent_srv.remove_rent_op(1, 1)
        self.assertEqual(len(self.__rent_srv.get_all_rentals()), 0)

    def test_get_list(self):
        self.__rent_srv.add_rent_op(1, 1)
        self.__rent_srv.add_rent_op(1, 2)
        freqs = self.__rent_srv.get_list_with_ids()
        self.assertEqual(freqs[1], 2) 

    def test_get_all_for_id1(self):
        self.__rent_srv.add_rent_op(1, 1)
        self.__rent_srv.add_rent_op(1, 2)
        rentals = self.__rent_srv.get_all_for_id1(1)
        self.assertEqual(len(rentals), 2)
        self.assertEqual(rentals[0].get_client_id(), 1)