Create database Magazinsportiv
go
use MagazinSportiv
go

CREATE TABLE Categorie
(IdC INT PRIMARY KEY,
NumeCategorie varchar(50)
)

CREATE TABLE Clienti
(IdCl INT PRIMARY KEY,
NumeClient varchar(100) NOT NULL,
Email varchar(100),
Adresa varchar(100),
Telefon varchar(100)
)

CREATE TABLE Comenzi
(IdC INT FOREIGN KEY REFERENCES Categorie(IdC),
IdCl INT FOREIGN KEY REFERENCES Clienti(IdCl),
CONSTRAINT pk_Comenzi PRIMARY KEY(IdC,IdCl),
Suma int,
Data DATE
)

CREATE TABLE Promotii
(IdPromotie INT PRIMARY KEY,
Nume varchar(100) NOT NULL,
Inceput DATETIME,
Sfarsit DATETIME,
Discount FLOAT
)

CREATE TABLE Depozit
(IdD INT PRIMARY KEY,
Nume varchar(100),
Adresa varchar(100),
Capacitate FLOAT
)

CREATE TABLE Angajati
(IdA INT PRIMARY KEY,
NumeAngajati varchar(100),
Rol varchar(100),
Salariu INT CHECK (Salariu>=2000 AND Salariu<=5000),
DataNasterii DATE,
Telefon varchar(100),
IdD INT FOREIGN KEY REFERENCES Depozit(IdD)
)

CREATE TABLE Furnizori
(IdF INT PRIMARY KEY,
NumeFurnizor varchar(100),
Adresa varchar(100)
)

CREATE TABLE Produse
(IdP INT PRIMARY KEY,
Nume varchar(100),
Brand varchar(100),
Pret float,
Stoc int CHECK(Stoc>=0 AND Stoc<=200),
Descriere varchar(100),
IdF INT FOREIGN KEY REFERENCES Furnizori(IdF),
IdPromotie INT FOREIGN KEY REFERENCES Promotii(IdPromotie),
IdA INT FOREIGN KEY REFERENCES Angajati(IdA)
)


CREATE TABLE Recenzii
(IdRecenzie INT PRIMARY KEY,
Data_recenziei DATETIME,
Nota INT CHECK(Nota>=1 AND Nota<=10),
IdP INT FOREIGN KEY REFERENCES Produse(IdP),
IdCl INT FOREIGN KEY REFERENCES Clienti(IdCl)
)

CREATE TABLE Metoda_de_Plata
(IdMet INT PRIMARY KEY,
Nume_Metoda varchar(100) CHECK(Nume_Metoda ='Cash' OR Nume_Metoda='Card'),
Taxa_procesare float,
IdP INT FOREIGN KEY REFERENCES Produse(IdP)
)