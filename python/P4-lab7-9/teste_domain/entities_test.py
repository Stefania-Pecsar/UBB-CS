import unittest

from domain.entities import *

class TestBooks(unittest.TestCase):
    def test_creare_carte(self):
        book=Carte(1,"Harry Potter","J.K.Rowling","o carte faina")
        self.assertEqual(book.get_id(),1)
        self.assertEqual(book.get_titlu(),"Harry Potter")
        self.assertEqual(book.get_descriere(),"O carte faina")
        self.assertEqual(book.get_autor(),"J.K.Rowling")

        book.set_titlu("Harry Potter z")
        book.set_descriere("O carte din aia")
        book.set_autor("Marin Preda")

        self.assertEqual(book.get_titlu("Harry Potter z"))
        self.assertEqual(book.get_descriere("O carte din aia"))
        self.assertEqual(book.get_autor("Marin Preda"))

    def test_eq_books(self):
        carte1=Carte(1,"Harry Potter","J.K.Rowling","o carte faina")
        carte2=Carte(1,"Harry Potter","J.K.Rowling","o carte faina")

        self.assertEqual(carte1,carte2)

        carte3=Carte(1,"Harry Potter","J.K.Rowling","o carte faina")

        self.assertNotEqual(carte1,carte3)

class TestClient(unittest.TestCase):
    def test_create_client(self):
        customer=Client(1,"Stefania Pecsar","6040608204989")

        self.assertEqual(customer.get_id(),1)
        self.assertEqual(customer.get_nume(),"Stefania Pecsar")
        self.assertEqual(customer.get_cnp(),"6040806204989")

        customer.set_nume("Stefania Pecsar")
        customer.setCNP("6040806204989")

        self.assertEqual(customer.get_nume(),"Stefania Pecsar")
        self.assertEqual(customer.get_cnp(),"6040806204989")

    def test_eq_clients(self):
        customer1=Client(1,"Stefania ","6040608204989")
        customer2=Client(1,"Stefania ","6040608204989")

        self.assertEqual(customer1,customer2)

        customer3=Client(1,"Stefania ","6040608204989")

        self.assertNotEqual(customer3,customer1)