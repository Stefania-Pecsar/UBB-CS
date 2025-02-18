from domain.entities import *
from domain.validatori import *
from repository.client_repo import *
import random
import string

class ClientService:
    def __init__(self,repo,validator):
        self.__repo=repo
        self.__validator=validator
        self.__clients=[]
        self.__index = 0

    def insert_client(self, nume, cnp):
        if self.__repo.get_all_clients() != []:
            list = self.__repo.get_all_clients()
            id_list = list[-1].get_id()
            self.__index = int(id_list) + 1
        else:
            self.__index = self.__index + 1
        id = self.__index
        customer=Client(id,nume,cnp)
        self.__validator.validate(customer)
        self.__repo.adauga_client(customer)
        return customer

    def erase_client(self,id):
        self.__repo.sterge_client(id)

    def modify_client(self,id,nume,cnp):
        customer=Client(id,nume,cnp)
        self.__validator.validate(customer)
        self.__repo.modifica_client(id,nume,cnp)
        return customer

    def search_by_id(self,id):
        customer=self.__repo.cauta_client_dupa_id(id)
        return customer

    def search_by_param(self,name,CNP):
        customer=self.__repo.cauta_client_dupa_parametru(name,CNP)
        return customer

    def adauga_random_clienti(self, numar):
        for _ in range(numar):
            random_id = Client_in_memorie.id 
            random_nume = ''.join(random.choice(string.ascii_letters) for _ in range(8))
            random_cnp = ''.join(random.choice(string.digits) for _ in range(13))

            client_nou = Client(
                id=random_id,
                nume=random_nume,
                cnp=random_cnp,
            )
            
            # Adăugați noul client în lista de clienți
            self.__clients.append(client_nou)
            # Incrementați ID-ul pentru a asigura unicitatea
            Client_in_memorie.id += 1

    def search_id(self,id):
        self.__repo.cauta_id(id)

    def get_all(self):
        return self.__clients

def test_insert_client():
    test_repo=Client_in_memorie()
    test_valid=ClientValidator()

    test_srv=ClientService(test_repo,test_valid)

    customer=test_srv.insert_client(1,"Stefania Pecsar","6040608204989")
    assert customer.get_id()==1
    assert customer.get_nume()=="Stefania Pecsar"
    assert customer.get_cnp()=="6040806204989"

    try:
        customer=test_srv.insert_client(1,"Stefania Pecsar","5040608204989")
        assert False
    except:
        assert True

def test_erase_client():
    test_repo=Client_in_memorie()
    test_valid=CartiValidator()

    test_srv=ClientService(test_repo,test_valid)

    customer1=test_srv.insert_client(1,"Stefania Pecsar","6040608204989")
    customer2=test_srv.insert_client(2,"Stefania Morar","6040608204988")

    test_srv.erase_client(2)
    assert len(test_srv.get_all_clients())==1

def test_modify_customer():
    test_repo=Client_in_memorie()
    test_valid=CartiValidator()

    test_srv=ClientService(test_repo,test_valid)

    customer1=test_srv.insert_client(1,"Stefania Pecsar","6040608204989")
    customer2=test_srv.insert_client(2,"Stefania Morar","6040608204988")

    mod_customer=test_srv.modify_customer(1,"Stefania Pecsar","6040608204989")
    assert mod_customer.get_id()==1
    assert mod_customer.get_nume()=="Stefania Pecsar"
    assert mod_customer.get_cnp()=="6040806204988"

    try:
        mod_customer=test_srv.insert_client(2,"","60408062046989")
        assert False
    except:
        assert True

def test_search_by_id():
    test_repo=Client_in_memorie()
    test_valid=ClientValidator()

    test_srv=ClientService(test_repo,test_valid)

    customer1=test_srv.insert_client(1,"Stefania Pecsar","6040608204989")
    customer2=test_srv.insert_client(2,"Stefania Pecsar","6040608204988")

    assert test_srv.search_by_id(1)==customer1
    assert test_srv.search_by_id(2)==customer2

    try:
        test_srv.search_by_id(3)
        assert False
    except ValueError:
        assert True

def test_search_by_param():
    test_repo=Client_in_memorie()
    test_valid=ClientValidator()

    test_srv=ClientService(test_repo,test_valid)

    customer1=test_srv.insert_client(1,"Stefania Pecsar","6040608204989")
    customer2=test_srv.insert_client(2,"Stefania Pecsar","6040608204988")

    assert test_srv.search_by_param("Stefania Pecasr","")==customer1
    assert test_srv.search_by_param("","6040806204989")==customer2

    try:
        test_srv.search_by_param("","")
        assert False
    except ValueError:
        assert True

    try:
        test_srv.search_by_param("Stefi","")
        assert False
    except ValueError:
        assert True

def test_get_all():
    test_repo=Client_in_memorie()
    test_valid=ClientValidator()

    test_srv=ClientService(test_repo,test_valid)

    customer1=test_srv.insert_client(1,"Stefania Pecsar","6040608204989")
    customer2=test_srv.insert_client(2,"Stefania Morar","6040608204988")

    assert len(test_srv.get_all())==2

def test_add_random():
    test_repo=Client_in_memorie()
    test_valid=ClientValidator()

    test_srv=ClientService(test_repo,test_valid)

    test_srv.adauga_random_clienti(5)

    assert len(test_srv.get_all_clients())==5