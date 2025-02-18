from domain.entities import *
from utils.utils import *

class CartiValidator:
    def validate(self,carte):
        erori=[]
        if carte.get_titlu()=="":
            erori.append("Titul nu poate fi vid")
        if carte.get_autor()=="":
            erori.append("Autor nu poate fi vid")
        if carte.get_descriere()=="":
            erori.append("Descrierea nu poate fi vida")
        if len(carte.get_descriere())>10000 :
            erori.append("Lungimea descrieri este prea mare")
        if len(erori)>0 :
            erori_string='\n'.join(erori)
            raise ValueError(erori_string)
        
class ClientValidator:
    def validate(self,client):
        erori=[]
        if client.get_nume()=="":
            erori.append("Numele nu poate fi vid")
        if client.get_cnp()=="":
            erori.append("CNP-ul nu poate fi vid")
        try:
            valoare=int(client.get_cnp())
        except:
            erori.append("CNP-ul nu este corect")
            valoare=0
        CNP=[]
        while valoare!=0:
            CNP.append(valoare%10)
            valoare//=10
        if len(CNP)>13:
            msg="Lungime invalida"+str(len(CNP))
            erori.append(msg)
        if len(erori)>0:
            erori_string='\n'.join(erori)
            raise ValueError(erori_string)
        
class InchirieriValidator:
    def validateInchirieri(self,inchirieri):
        erori = []
        if int(inchirieri.get_inchirieri()) < 0 or int(inchirieri.getInchirieri()) > 100:
            erori.append('O carte poate fi inchiriata intre 1 si 100 ori')
        if len(erori)>0:
            erori_string='\n'.join(erori)
            raise ValueError(erori_string)