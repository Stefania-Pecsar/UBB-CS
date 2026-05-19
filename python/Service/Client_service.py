from Domain.Entities import Client
from Domain.Validators import ClientValidator
from Repository.ClientRepo import ClientRepo
import random
import string

class ClientService():
    def __init__(self,repo,validator):
        """
        Atribuie service-ului o regula de validare si un repo
        Controller GRASP
        """
        self.__repo=repo
        self.__validator=validator
        self.__clients=[]

    def insert_client(self,id,name,cnp):
        """
        Insereraza un client nou in repo
        :param id: id-ul unic al clientului
        :param name: numele clientului
        :param cnp: cnp-ul clientului
        :return: filmul nou adaugat
        :raises: ValueErorr pentru date invalide
        """
        customer=Client(id,name,cnp)
        self.__validator.validate(customer)
        self.__repo.adauga_client(customer)
        return customer
    
    def adauga_random_clienti(self, numar):
        for _ in range(numar):
            random_id = len(self.__repo.get_all_clients()) + 1
            random_nume = ''.join(random.choice(string.ascii_letters) for _ in range(8))
            random_cnp = ''.join(random.choice(string.digits) for _ in range(13))

            client_nou = Client(
                id=random_id,
                nume=random_nume,
                cnp=random_cnp,
            )
            self.__repo.adauga_client(client_nou) 
 

    def erase_client(self,id):
        """
        Sterge clientul cu id-ul id
        :param id: id-ul clientului de sters
        """
        self.__repo.delete_client(id)

    def modify_customer(self,id,name,cnp):
        """
        Modifica clientul
        :param id:id-ul clientului de modificat
        :param name:numele clientului de modificat
        :param cnp:cnp-ul clientului de modificat
        :return: clientul modificat
        :raises: ValueErorr pentru date invalide
        """
        customer=Client(id,name,cnp)
        self.__validator.validate(customer)
        self.__repo.modify_client(id,name,cnp)
        return customer

    def search_by_id(self,id):
        """
        Cauta clientul in repo dupa id
        :param id: id-ul de cautat
        :return: clientul cautat
        :raises: ValueError daca id-ul cautat nu este valid
        """
        customer=self.__repo.cauta_client_dupa_id(id)
        return customer

    def search_by_param(self,name):
        """
        Cauta clientul dupa parametrii
        :param name: numele clientului
        :return: clientul cautat
        :raises: ValueError daca clientul cautat nu este gasit
        """
        customer=self.__repo.cauta_client_dupa_parametru(name)
        return customer


    def search_id(self,id):
        """
        Verifica daca id-ul unui client este valid
        :param id: id-ul clientului
        :raises: ValueError daca clientul nu este gasit
        """
        self.__repo.cauta_client_dupa_id(id)

    def get_all(self):
        """
        Returneaza lista de clienti
        """
        return self.__repo.get_all_clients()

    def afisare_clienti(self):
        """
        Returneaza lista de clienti.
        """
        return self.get_all()