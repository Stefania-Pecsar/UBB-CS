from repository.inchiriere_repo import *
from repository.client_repo import *
from repository.carte_repo import *

class RentService():
    def __init__(self,repo):
        self.__repo=repo

    def add_rent_op(self,id1,id2):
        self.__repo.adauga_inchirieri(id1,id2)

    def remove_rent_op(self,id1,id2):
        self.__repo.sterge_inchirieri(id1,id2)

    def get_list_with_ids(self):
        return self.__repo.get_list()

    def get_list_with_id_max(self):
        return self.__repo.get_all_for_max()

    def get_all_for_id1(self,id):
        return self.__repo.get_all_id1(id)

    def get_all_for_id2(self,id):
        return self.__repo.get_all_id2(id)