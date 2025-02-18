import unittest

from domain.entities import *
from domain.validatori import *
from repository.carte_repo import *
from service.service_carti import *

class TestBookService(unittest.TestCase):
    def setUp(self) -> None:
        self.__test_valid=CartiValidator()
        self.__test_repo=Carte_in_memorie()
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
        self.assertEqual(book1.get_titlu(),"Razboiul celor 2 roxe")
        self.assertEqual(book1.get_autor(),"Conn Iggulden")
        self.assertEqual(book1.get_titlu(),"carte ostorica")
        self.assertRaises(ValueError,self.__test_srv.modify_carte,1,"","Conn Iggulden","carte istorica")

    def test_get_all(self):
        carte1=self.__test_srv.insert_carte(1,"Harry Potter","J.K.Rowling","o carte faina")
        carte2=self.__test_srv.insert_carte(2,"Pasarea Spin","Colleen McCullough")

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

    def test_random_carti(self):
        self.__test_srv.adauga_random_carti(5)

        self.assertEqual(len(self.__test_srv.get_all()),5)