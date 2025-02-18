import unittest

from Domain.Entities import *
from Repository.CartiRepo import *
from Repository.ClientRepo import *
from Repository.InchirieriRepo import *

class TesteCartiRepo(unittest.TestCase):
    def setUp(self)->None:
        self.__repo=CarteRepo()
        self.__repo1=CarteRepo()
        self.__repo2=CarteRepo()
        self.__repo3=CarteRepo()
        self.__new_repo=CarteRepo()

    def test_eq(self):
        book=Carte(1,"Harry Potter","J.K.Rowling","o carte faina")
        book1=Carte(1,"Harry Potter","J.K.Rowling","o carte faina")


        self.__repo1.adauga_carte(book)
        self.__repo2.adauga_carte(book)
        self.assertEqual(self.__repo1,self.__repo2)

        self.__repo3.adauga_carte(book1)
        self.assertNotEqual(self.__repo1,self.__repo3)
        self.assertRaises(ValueError,self.__repo1.cauta_id,5)

    def test_adauga_carte(self):
        book=Carte(1,"Harry Potter","J.K.Rowling","o carte faina")

        self.__repo.adauga_carte(book)

        self.assertEqual(len(self.__repo.get_all_books()),1)

    def test_sterge_carte(self):
        book=Carte(1,"Harry Potter","J.K.Rowling","o carte faina")

        self.__repo.adauga_carte(book)
        self.__repo.sterge_carte(1)

        self.assertEqual(len(self.__repo.get_all_books()),0)

    def test_modifica_carte(self):
        book=Carte(1,"Harry Potter","J.K.Rowling","o carte faina")

        self.__repo.adauga_carte(book)
        self.__repo.modifica_carte(1,"Harry Potter z","J.K.R. rowling","o carte rea")

        book2=Carte(1,"Harry Potter z","J.K.R. rowling","o carte rea")
        self.__new_repo.adauga_carte(book2)

        self.assertEqual(self.__repo,self.__new_repo)

    def test_get_all_books(self):
        book=Carte(1,"Harry Potter","J.K.Rowling","o carte faina")

        self.__repo.adauga_carte(book)

        self.assertEqual(self.__repo.get_all_bookss(),[book])

    def test_search_by_id(self):
        book=Carte(1,"Harry Potter","J.K.Rowling","o carte faina")
        self.__repo.adauga_carte(book)

        book=Carte(2,"Harry Potter z","J.K.R. rowling","o carte rea")
        self.__repo.adauga_carte(book)
        self.assertEqual(self.__repo.cauta_carte_dupa_id(2),book)
        self.assertEqual(self.__repo.cauta_carte_dupa_id(1).get_titlu(),"Harry Potter")
        self.assertRaises(ValueError,self.__repo.cauta_carte_dupa_id,3)

    def test_search_by_param(self):
        book=Carte(1,"Harry Potter","J.K.Rowling","o carte faina")
        self.__repo.adauga_carte(book)

        book1=Carte(2,"Harry Potter z","J.K.R. rowling","o carte rea")
        self.__repo.adauga_carte(book1)

        self.assertEqual(self.__repo.cauta_carte_dupa_parametru("Harry Potter","",""),book)
        self.assertEqual(self.__repo.cauta_carte_dupa_parametru("","J.K.R. rowling",""),book1)
        self.assertEqual(self.__repo.cauta_carte_dupa_parametru("","","o carte rea"),book1)
        self.assertRaises(ValueError,self.__repo.cauta_carte_dupa_parametru,"","","")
        self.assertRaises(ValueError,self.__repo.cauta_carte_dupa_parametru,"HP","JKR","o carte")


class TestClientRepo(unittest.TestCase):

    def setUp(self) -> None:
        self.__repo=ClientRepo()
        self.__repo1=ClientRepo()
        self.__repo2=ClientRepo()
        self.__repo3=ClientRepo()
        self.__new_repo=ClientRepo()

    def test_eq(self):
        customer1=Client(1,"Pecsar Stefania","6040806204989")
        customer2=Client(1,"Pecsar Stefania","6040806204989")

        self.__repo1.adauga_client(customer1)
        self.__repo2.adauga_client(customer1)
        self.assertEqual(self.__repo1,self.__repo2)
        self.__repo3.adauga_client(customer2)
        self.assertNotEqual(self.__repo1,self.__repo3)
        self.assertRaises(ValueError,self.__repo3.cauta_id,5)

    def test_add_client(self):
        customer=Client(1,"Pecsar Stefania","6040806204989")

        self.__repo.adauga_client(customer)
        self.assertEqual(len(self.__repo.get_all_clients()),1)

    def test_delete_client(self):
        customer=Client(1,"Pecsar Stefania","6040806204989")

        self.__repo.adauga_client(customer)
        self.__repo.sterge_client(1)
        self.assertEqual(len(self.__repo.get_all_clients()),0)

    def test_modify_client(self):
        customer=Client(1,"Pecsar Stefania","6040806204989")

        self.__repo.adauga_client(customer)
        self.__repo.modifica_client(1,"Morar Stefana","6040806204989")

        customer2=Client(1,"Morar Stefana","6040806204989")

        self.__new_repo.adauga_client(customer2)
        self.assertEqual(self.__repo,self.__new_repo)

    def test_get_all_clients(self):
        customer=Client(1,"Pecsar Stefana","6040806204989")

        self.__repo.adauga_client(customer)
        self.assertEqual(self.__repo.get_all_clients(),[customer])

    def test_search_client_by_id(self):
        customer1=Client(1,"Pecsar Stefania","6040806204989")
        customer2=Client(2,"Morar Stefana","6040806204989")

        self.__repo.adauga_client(customer1)
        self.__repo.adauga_client(customer2)

        self.assertEqual(self.__repo.cauta_client_dupa_id(1),customer1)
        self.assertEqual(self.__repo.cauta_client_dupa_id(2),customer2)
        self.assertRaises(ValueError,self.__repo.cauta_client_dupa_id,3)

    def test_search_client_by_param(self):
        customer1=Client(1,"Pecsar Stefania","6040806204989")
        customer2=Client(2,"Morar Stefana","6040806204989")

        self.__repo.adauga_client(customer1)
        self.__repo.adauga_client(customer2)

        self.assertEqual(self.__repo.cauta_client_dupa_parametru("morar Stefana",""),customer2)
        self.assertEqual(self.__repo.cauta_client_dupa_parametru("","640806204989"),customer1)
        self.assertRaises(ValueError,self.__repo.cauta_client_dupa_parametru,"Stefi","")

class TestRentRepo(unittest.TestCase):
    def setUp(self) -> None:
        self.__repo_rent=Inchirieri()

    def test_adauga_inchirieri(self):
        self.__repo_rent.adauga_inchirieri(1,1)
        self.assertEqual(self.__repo_rent.get_all(),[(1,1)])

    def test_sterge_inchirieri(self):
        self.__repo_rent.adauga_inchirieri(1,1)
        self.assertEqual(self.__repo_rent.get_all(),[(1,1)])

        self.__repo_rent.sterge_inchirieri(1,1)
        self.assertEqual(self.__repo_rent.get_all(),[])

    def test_get_list(self):
        self.__repo_rent.adauga_inchirieri(1,2)
        self.__repo_rent.adauga_inchirieri(1,3)
        self.__repo_rent.adauga_inchirieri(2,4)
        self.__repo_rent.adauga_inchirieri(5,3)

        lst=self.__repo_rent.get_list()

        self.assertEqual(lst,[0,2,1,0,0,1]+[0]*94)

    def test_get_all_id(self):
        self.__repo_rent.adauga_inchirieri(1,1)
        self.__repo_rent.adauga_inchirieri(1,2)
        self.assertEqual(self.__repo_rent.get_all_id1(1),[1,2])

    def test_last(self):
        self.__repo_rent.adauga_inchirieri(1,2)
        self.__repo_rent.adauga_inchirieri(1,3)
        self.__repo_rent.adauga_inchirieri(2,4)
        self.__repo_rent.adauga_inchirieri(5,3)

        lst=self.__repo_rent.get_all_for_max()

        self.assertEqual(lst,[1,5])