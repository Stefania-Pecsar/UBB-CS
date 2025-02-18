import unittest

from domain.entities import *
from domain.validatori import *

class CValidatori(unittest.TestCase):
    def setUp(self) -> None:
        self.__valid=CartiValidator()

    def test_carte(self):
        carte=Carte(1,"Harry Potter","J.K.Rowling","o carte faina")
        self.__valid.validate(carte)

        carte1=Carte(1,"","J.K.Rowling","o carte faina")
        self.assertRaises(ValueError,self.__valid.validate,carte1)

        carte2=Carte(1,"Harry Potter","","o carte faina")
        self.assertRaises(ValueError,self.__valid.validate,carte2)

        carte3=Carte(1,"Harry Potter","J.K.Rowling","")
        self.assertRaises(ValueError,self.__valid.validate,carte3)

class CValidatori(unittest.TestCase):
    def setUp(self) -> None:
        self.__valid=ClientValidator()

    def test_client(self):
        customer=Client(1,"Stefania ","6040608204989")
        self.__valid.validate(customer)

        customer1=Client(1,"","6040608204989")
        self.assertRaises(ValueError,self.__valid.validate,customer1)

        customer3=Client(1,"Stefania ","")
        self.assertRaises(ValueError,self.__valid.validate,customer3)