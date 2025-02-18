from termcolor import colored

class Carte:
    def __init__ (self,id,titlu,autor,descriere):
        self.__id = id
        self.__titlu = titlu
        self.__autor = autor
        self.__descriere = descriere
        
    def get_id(self):
        return self.__id
    
    def get_titlu(self):
        return self.__titlu
    
    def get_autor(self):
        return self.__autor
    
    def get_descriere(self):
        return self.__descriere
    
    def set_titlu(self,valoare):
        self.__titlu=valoare

    def set_descriere(self,valoare):
        self.__descriere=valoare

    def set_autor(self,valoare):
        self.__autor=valoare

    def __repr__(self):
        return colored("Id: ","magenta")+str(self.__id)+colored(" Titlu: ","magenta")+str(self.__titlu)+colored(" Autor: ","magenta")+str(self.__autor)+colored(" Descriere: ","magenta")+str(self.__descriere)

    def __eq__(self, other):
        return (self.__id==other.__id
                and self.__descriere==other.__descriere 
                and self.__titlu==other.__titlu
                and self.__autor==other.__autor)

class Client:
    def __init__ (self,id,nume,cnp):
        self.__id=id
        self.__nume=nume
        self.__cnp=cnp

    def get_id(self):
        return self.__id
    
    def get_nume(self):
        return self.__nume
    
    def get_cnp(self):
        return self.__cnp
    
    def set_id(self,valoare):
        self.__id=valoare

    def set_nume(self,valoare):
        self.__nume=valoare

    def set_cnp(self,valoare):
        self.__cnp=valoare

    def __repr__(self):
        return colored("Nume: ","magenta")+str(self.__nume)+colored(" CNP: ","magenta")+str(self.__cnp)

    def __eq__(self, other):
        return self.__id == other.__id and self.__nume == other.__nume and self.__cnp == other.__cnp

