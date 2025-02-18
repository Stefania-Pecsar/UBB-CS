from Repository.CartiRepo import CarteFileRepo
from Repository.ClientRepo import ClientsFileRepo
from Repository.InchirieriRepo import Inchirieri
from Service.Client_service import ClientService
from Service.Carti_service import CarteService
from Service.InchirieriService import RentService
from Domain.Validators import CartiValidator, ClientValidator
from Ui.Console import console



Book=CarteService(CarteFileRepo("books.txt"),CartiValidator())
Customer=ClientService(ClientsFileRepo("client.txt"),ClientValidator())
Rent=RentService(Inchirieri())


ui=console(Book,Customer,Rent)
ui.main()