import unittest

from domain.entities import *
from repository.carte_repo import *

class TesteCartiInMemorie(unittest.TestCase):
    def setUp(self)->None:
        self.__repo=Carte_in_memorie()
        self.__repo1=Carte_in_memorie()
        self.__repo2=Carte_in_memorie()
        self.__repo3=Carte_in_memorie()
        self.__new_repo=Carte_in_memorie()

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