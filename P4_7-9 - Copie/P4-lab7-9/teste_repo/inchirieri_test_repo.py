import unittest

from repository.inchiriere_repo import *

class TestRentRepo(unittest.TestCase):
    def setUp(self) -> None:
        self.__repo_rent=Inchirieri_in_memorie()

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