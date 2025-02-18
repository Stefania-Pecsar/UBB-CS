import unittest

from domain.entities import *
from repository.client_repo import *

class TestClientRepo(unittest.TestCase):

    def setUp(self) -> None:
        self.__repo=Client_in_memorie()
        self.__repo1=Client_in_memorie()
        self.__repo2=Client_in_memorie()
        self.__repo3=Client_in_memorie()
        self.__new_repo=Client_in_memorie()

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

class RepoFileTest(unittest.TestCase):

    def setUp(self) -> None:
        self.__repo=ClientsFileRepo("test_clients.txt")
        
    def test_create_file_Repo(self):
        init_len=len(self.__repo.get_all_clients())
        customer=Client(5,"Pecsar Stefania","6040806204989")
        self.__repo.adauga_client(customer)

        self.assertEqual(len(self.__repo.get_all_clients()),init_len+1)

    def test_modify_fileRepo(self):
        init_len=len(self.__repo.get_all_clients())
        customer=Client(1,"Pecsar Stefania","6040806204989")

        self.__repo.adauga_client(customer)
        self.__repo.modifica_client(1,"Morar Stefana","6040806204989")

        self.assertEqual(len(self.__repo.get_all_clients()),init_len+1)