USE Magazinsportiv

--Crearea tabelelor care sunt legate de View
DELETE FROM Tables
SET IDENTITY_INSERT Tables ON;
INSERT INTO Tables(TableID,Name) VALUES
	(1, 'Categorie'),
	(2, 'Clienti'),
	(3, 'MagazinCategorieClienti');
SET IDENTITY_INSERT Tables OFF;

--Cream un View pt un singur tabel (PK)
CREATE OR ALTER VIEW View_Categorie AS
	SELECT IdC AS ID_Categorie, 
    NumeCategorie AS DenumireCategorie
FROM Categorie;

--Cream un View pentru cele 2 tabele (PK+FK)
CREATE OR ALTER VIEW View_CategorieClienti AS
SELECT cl.NumeClient AS NumeClient,
    cl.Email AS Email,
    cl.Adresa AS Adresa,
    cl.Telefon AS Telefon,
    c.NumeCategorie AS Categorie
FROM Clienti cl INNER JOIN Comenzi com ON cl.IdCl = com.IdCl INNER JOIN Categorie c ON com.IdC = c.IdC;

--Cream un View ce contine o comanda SELECT pe cel putin 2 tabele
-- si avand o clauza GROUP BY
CREATE OR ALTER VIEW View_MagazinCategorieClienti AS
SELECT c.NumeCategorie AS Categorie,
    cl.NumeClient AS Client,
    SUM(CAST(com.Suma AS BIGINT)) AS TotalSuma,
    COUNT(com.Data) AS NrComenzi
FROM Categorie c INNER JOIN Comenzi com ON c.IdC = com.IdC INNER JOIN Clienti cl ON com.IdCl = cl.IdCl
GROUP BY c.NumeCategorie, cl.NumeClient;

--In View adaugam View-urile create mai sus
SET IDENTITY_INSERT Views ON;
INSERT INTO Views(ViewID, Name) VALUES
	(1, 'View_Client'),
	(2, 'View_ComandaClient'),
	(3, 'View_Comenzi_Clienti_Suma');
SET IDENTITY_INSERT Views OFF;

--Testele pe care le am ( ca si optiuni ) pentru tabele
SET IDENTITY_INSERT Tests ON;
DELETE FROM Tests;
INSERT INTO Tests(TestID, Name) VALUES
	(1, 'selectView'),
    (2, 'insertCategorie'),
    (3, 'insertClienti'),
    (4, 'insertComenzi'),
    (5, 'deleteCategorie'),
    (6, 'deleteClienti'),
    (7, 'deleteComenzi');
SET IDENTITY_INSERT Tests OFF;

--Testele pentru View
INSERT INTO TestViews (TestID, ViewID) VALUES
	(1, 1),
	(1, 2),
	(1, 3);

--Testele pentru tabele in ordinea corespunzatoare
SELECT * FROM TestTables;
INSERT INTO TestTables(TestID, TableID, NoOfRows, Position) VALUES
    (2, 1, 10000, 1), -- insertCategorie
    (3, 2, 10000, 2), -- insertClienti
    (6, 3, 10000, 3), -- insertComenzi
    (7, 3, 10000, 4), -- deleteComenzi
    (5, 2, 10000, 5), -- deleteClienti
    (4, 1, 10000, 6); -- deleteCategorie
	
--Verificari
SELECT * FROM View_Categorie;
SELECT * FROM View_CategorieClienti;
SELECT * FROM View_MagazinCategorieClienti;

SELECT * FROM Tables;
SELECT * FROM Views;
SELECT * FROM Tests;
SELECT * FROM TestTables;
SELECT * FROM TestRunTables;
SELECT * FROM TestRunViews;

