CREATE DATABASE Practic
GO
USE Practic
GO
	
		--creare
CREATE TABLE Biblioteca
(IdB INT PRIMARY KEY not null,
Denumire varchar(100),
AnInfiintare INT,
Oras varchar(100),
Strada varchar (100),
Numar INT
)

CREATE TABLE Copii
(IdCopil INT PRIMARY KEY not null,
Nume varchar(50),
Prenume varchar(50),
Gen varchar(50),
DataNasterii DATE
)

CREATE TABLE Carti
(IdC INT PRIMARY KEY not null,
Titlu varchar(100),
Editura varchar(100),
AnAparitie INT,
IdB INT FOREIGN KEY REFERENCES Biblioteca(IdB)
)

CREATE TABLE Povesti
(IdP INT PRIMARY KEY not null,
Denumire varchar(100),
Autor varchar(50),
AnulScrierii INT,
NrPag INT,
IdC INT FOREIGN KEY REFERENCES Carti(IdC)
)

CREATE TABLE Ranking
(IdCopil INT FOREIGN KEY REFERENCES Copii(IdCopil),
IdP INT FOREIGN KEY REFERENCES Povesti(IdP),
CONSTRAINT pk_Comenzi PRIMARY KEY(IdCopil,IdP),
NrPuncte INT CHECK (NrPuncte>=0 AND NrPuncte<=5),
Durata INT
)

		--insert
INSERT INTO Biblioteca(IdB,Denumire,AnInfiintare,Oras,Strada,Numar) VALUES
	(1, 'Biblioteca Judeteana',1958,'Hunedoara','Traian',27),
	(2, 'Biblioteca Universitara',1944,'Cluj','Hasdeu',5);

SELECT * FROM Biblioteca

INSERT INTO Copii(IdCopil,Nume,Prenume,Gen,DataNasterii) VALUES
	(1, 'Pecsar', 'Stefania', 'feminin','2004-08-06'),
	(2, 'Pecsar','Tudor','masculin','2010-07-17'),
	(3, 'Stroe', 'Bogdan', 'masculin', '2003-03-14'),
	(4, 'Marchidanu', 'Bogdan','masculin','2010-10-04');

SELECT * FROM Copii

INSERT INTO Carti(IdC,Titlu,Editura,AnAparitie,IdB) VALUES
	(1,'HP','Arthur',2007,1),
	(2, 'A', 'B', 1987,2),
	(3, 'Dada', 'Fericirea',2004,2),
	(4, 'Ubb','Cluj',1885,1);

SELECT * FROM Carti

INSERT INTO Povesti(IdP,Denumire,Autor,AnulScrierii,NrPag,IdC) VALUES 
	(1,'PF','jkr',2003,100,1),
	(2,'BD','idk',1880,500,4),
	(3, 'shdbdsj','hs',2000,300,3),
	(4, 'TM','jkr',2006,546,1),
	(5, 'MAP','shhj',1882,45,4);

SELECT * FROM Povesti

INSERT INTO Ranking(IdCopil,IdP,NrPuncte,Durata) VALUES
	(1,5,4,20),
	(3,4,0,10),
	(2,5,5,60),
	(1,2,2,100),
	(4,2,1,22);

SELECT * FROM Ranking

		--view
CREATE OR ALTER VIEW TopPovesti AS
SELECT p.Denumire,COUNT(r.IdCopil) AS CopiiCitesc
FROM Povesti p
INNER JOIN Ranking r ON p.IdP = r.IdP
GROUP BY p.Denumire
HAVING COUNT(r.IdCopil) > 1;

SELECT * FROM TopPovesti

		--procedura
GO
CREATE OR ALTER FUNCTION VALIDARE (
	@IdCopil INT,
	@IdP INT,
	@NrPuncte INT,
	@Durata INT
	)RETURNS INT AS BEGIN

	DECLARE @IdCopil_count INT;
	SELECT @IdCopil_count = COUNT(*) FROM Copii WHERE IdCopil = @IdCopil

	DECLARE @IdP_count INT;
	SELECT @IdP_count = COUNT(*) FROM Povesti WHERE IdP = @IdP

	IF @Durata IS NULL OR @IdCopil_count = 0 OR @IdP_count = 0
		RETURN 0;
	RETURN 1;
END
GO

GO
CREATE OR ALTER PROCEDURE Evaluare
	@IdCopil INT,
	@IdP INT,
	@NrPuncte INT,
	@Durata INT
AS BEGIN
	DECLARE @validation_status INT;
	SELECT @validation_status = dbo.VALIDARE(@IdCopil,@IdP,@NrPuncte,@Durata);
	IF (@validation_status = 0)
	BEGIN
		RAISERROR(N'Au fost introduse gresit datele', 16, 1);
		RETURN;
	END

	--insert
	INSERT INTO Ranking(IdCopil,IdP,NrPuncte,Durata)
		VALUES (@IdCopil,@IdP,@NrPuncte,@Durata);
	SELECT * FROM Ranking
	PRINT(N'Conexiunea a fost creata cu succes!');

	--print
	SELECT * FROM Ranking
	WHERE IdCopil = @IdCopil and IdP = @IdP;
	PRINT(N'Print!')

	--actualizare
	UPDATE Ranking
	SET Durata = 1 + @Durata , NrPuncte =@NrPuncte + 1
	WHERE IdCopil = @IdCopil AND IdP = @IdP;
	SELECT * FROM Ranking
	PRINT(N'Conexiunea a fost modificata cu succes!');

	--stergere
	DELETE FROM Ranking
	WHERE IdCopil = @IdCopil AND IdP = @IdP;
	SELECT * FROM Ranking
	PRINT(N'Stergere!')

END
go

EXEC Evaluare 4,1,1,20