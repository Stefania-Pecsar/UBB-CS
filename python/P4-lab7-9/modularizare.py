from domain.entities import *
from domain.validatori import *
from repository.client_repo import *
from repository.carte_repo import *
from repository.inchiriere_repo import *
from service.service_inchirieri import *
from service.service_clienti import *
from service.service_carti import *
from ui.console import console

Book=CarteService(CarteFileRepo("books.txt"),CartiValidator())
Customer=ClientService(ClientsFileRepo("client.txt"),ClientValidator())
Rent=RentService(Inchirieri_in_memorie())

ui=console(Book,Customer,Rent)

ui.main()