import unittest

from domain.entities import *
from domain.validatori import *
from repository.client_repo import *
from service.service_clienti import *

class ClientServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.__test_repo=Client_in_memorie()
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

    def test_add_random(self):
        self.__test_srv.adauga_random_clienti(5)

        self.assertEqual(len(self.__test_srv.get_all()),5)