Create database Placereaceaiului
go
use Ceai
go

CREATE TABLE Magazine
(Mid INT PRIMARY KEY,
Denumire varchar(50),
NrMagazine int,
NrClienti int)

CREATE TABLE Tipuri
(Tid INT PRIMARY KEY IDENTITY,
Tip varchar(50) DEFAULT 'Negru',
NeCeaiuri int)

CREATE TABLE Ceaiuri
(Cid INT PRIMARY KEY IDENTITY,
Denumire
)

