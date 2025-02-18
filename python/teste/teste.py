import unittest
import os
from Repository.CartiRepo import *
from Repository.ClientRepo import *

class TestCarteFileRepo(unittest.TestCase):

    def setUp(self) -> None:
        self.__repo = CarteFileRepo("test_carti.txt")
        self.__new_repo = CarteFileRepo("test_carti.txt")

    def tearDown(self) -> None:
        if os.path.exists("test_carti.txt"):
            os.remove("test_carti.txt")

    def test_load_from_file(self):
        with open("test_carti.txt", "w") as f:
            f.write("1;Harry Potter;J.K.Rowling;o carte faina\n")
            f.write("2;1984;George Orwell;un roman distopic\n")
        
        repo = CarteFileRepo("test_carti.txt")
        books = repo.get_all_books()
        self.assertEqual(len(books), 2)
        self.assertEqual(books[0].get_titlu(), "Harry Potter")
        self.assertEqual(books[1].get_autor(), "George Orwell")

    def test_save_to_file(self):
        book = Carte(1, "Harry Potter", "J.K.Rowling", "o carte faina")
        self.__repo.adauga_carte(book)
        self.__repo._CarteFileRepo__save_to_file()

        with open("test_carti.txt", "r") as f:
            content = f.readlines()
        
        self.assertEqual(len(content), 1)
        self.assertIn("1;Harry Potter;J.K.Rowling;o carte faina", content[0])

    def test_load_empty_file(self):
        with open("test_carti.txt", "w") as f:
            f.write("")
        
        repo = CarteFileRepo("test_carti.txt")
        books = repo.get_all_books()
        self.assertEqual(len(books), 0)

    def test_save_empty_repo(self):
        self.__repo._CarteFileRepo__save_to_file()

        with open("test_carti.txt", "r") as f:
            content = f.read()
        
        self.assertEqual(content, "")

    def test_load_file_with_invalid_format(self):
        with open("test_carti.txt", "w") as f:
            f.write("1;Harry Potter;J.K.Rowling\n")  # Missing description
        
        repo = CarteFileRepo("test_carti.txt")
        self.assertRaises(ValueError, repo.get_all_books)

    def test_save_multiple_books_to_file(self):
        book1 = Carte(1, "Harry Potter", "J.K.Rowling", "o carte faina")
        book2 = Carte(2, "1984", "George Orwell", "un roman distopic")
        self.__repo.adauga_carte(book1)
        self.__repo.adauga_carte(book2)
        self.__repo._CarteFileRepo__save_to_file()

        with open("test_carti.txt", "r") as f:
            content = f.readlines()
        
        self.assertEqual(len(content), 2)
        self.assertIn("1;Harry Potter;J.K.Rowling;o carte faina", content[0])
        self.assertIn("2;1984;George Orwell;un roman distopic", content[1])

class TestClientRepo(unittest.TestCase):

    def setUp(self) -> None:
        self.__repo = ClientsFileRepo("test_clienti.txt")
        self.__new_repo = ClientsFileRepo("test_clienti.txt")

    def tearDown(self) -> None:
        if os.path.exists("test_clienti.txt"):
            os.remove("test_clienti.txt")

    # Test pentru încărcarea din fișier
    def test_load_from_file(self):
        with open("test_clienti.txt", "w") as f:
            f.write("1;Pecsar Stefania;6040806204989\n")
            f.write("2;Morar Stefana;6040806204990\n")
        
        repo = ClientsFileRepo("test_clienti.txt")
        clients = repo.get_all_clients()
        self.assertEqual(len(clients), 2)
        self.assertEqual(clients[0].get_nume(), "Pecsar Stefania")
        self.assertEqual(clients[1].get_cnp(), "6040806204990")

    # Test pentru salvarea în fișier
    def test_save_to_file(self):
        client = Client(1, "Pecsar Stefania", "6040806204989")
        self.__repo.adauga_client(client)
        self.__repo._ClientsFileRepo__save_in_file()

        with open("test_clienti.txt", "r") as f:
            content = f.readlines()
        
        self.assertEqual(len(content), 1)
        self.assertIn("1;Pecsar Stefania;6040806204989", content[0])

    # Test pentru încărcarea unui fișier gol
    def test_load_empty_file(self):
        with open("test_clienti.txt", "w") as f:
            f.write("")
        
        repo = ClientsFileRepo("test_clienti.txt")
        clients = repo.get_all_clients()
        self.assertEqual(len(clients), 0)

    # Test pentru salvarea unui repo gol
    def test_save_empty_repo(self):
        self.__repo._ClientsFileRepo__save_in_file()

        with open("test_clienti.txt", "r") as f:
            content = f.read()
        
        self.assertEqual(content, "")

    # Test pentru încărcarea unui fișier cu format invalid
    def test_load_file_with_invalid_format(self):
        with open("test_clienti.txt", "w") as f:
            f.write("1;Pecsar Stefania;6040806204989\n")  # Missing CNP

        repo = ClientsFileRepo("test_clienti.txt")
        self.assertRaises(ValueError, repo.get_all_clients)

    # Test pentru salvarea mai multor clienți în fișier
    def test_save_multiple_clients_to_file(self):
        client1 = Client(1, "Pecsar Stefania", "6040806204989")
        client2 = Client(2, "Morar Stefana", "6040806204990")
        self.__repo.adauga_client(client1)
        self.__repo.adauga_client(client2)
        self.__repo._ClientsFileRepo__save_in_file()

        with open("test_clienti.txt", "r") as f:
            content = f.readlines()
        
        self.assertEqual(len(content), 2)
        self.assertIn("1;Pecsar Stefania;6040806204989", content[0])
        self.assertIn("2;Morar Stefana;6040806204990", content[1])