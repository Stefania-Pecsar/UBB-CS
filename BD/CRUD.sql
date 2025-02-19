USE Magazinsportiv

-- Functie de validare pentru Clienti
GO
CREATE OR ALTER FUNCTION Validare_Clienti(
	@IdCl INT, --PK
	@NumeClient VARCHAR(100),
	@Email VARCHAR(100),
	@Adresa VARCHAR(100),
	@Telefon VARCHAR(100)
	)RETURNS INT AS BEGIN
	--Verificam daca mai exista vreun obiect cu acest id 
	DECLARE @idCl_count INT;
	SELECT @idCl_count =COUNT(*) FROM Clienti WHERE IdCl = @IdCl;

	IF @NumeClient IS NULL OR @Email IS NULL OR @Adresa IS NULL OR @Telefon IS NULL OR(@idCl_count IS NOT NULL AND @idCl_count > 0)
		RETURN 0

	RETURN 1
END
GO

GO
CREATE OR ALTER PROCEDURE CRUD_Clienti
	@IdCl INT, 
	@NumeClient VARCHAR(100),
	@Email VARCHAR(100),
	@Adresa VARCHAR(100),
	@Telefon VARCHAR(100)
AS BEGIN
	DECLARE @validation_status INT;
	SELECT @validation_status = dbo.Validare_Clienti(@IdCl,@NumeClient,@Email,@Adresa,@Telefon);
	IF (@validation_status = 0)
	BEGIN
		RAISERROR(N'Au fost introduse date incorecte', 16, 1);
		RETURN;
	END

	--CREATE = INSERT
	INSERT INTO Clienti(IdCl,NumeClient,Email,Adresa,Telefon)
		VALUES (@IdCl,@NumeClient,@Email,@Adresa,@Telefon);
	SELECT * FROM Clienti
	PRINT(N'Clientul a fost creata cu succes! Folosim id-ul de client '+ CAST(@IdCl AS VARCHAR(20))+' !');

	--READ = SELECT
	SELECT * FROM Clienti
	WHERE IdCl = @IdCl;
	PRINT(N'Clientul a fost printata cu succes cu id-ul ' + CAST(@IdCl AS VARCHAR(100)) + ' !');

	--UPDATE
	UPDATE Clienti
	SET Adresa = 'Update' + @Adresa
	WHERE IdCl = @IdCl;
	SELECT * FROM Clienti
	PRINT(N'Clientul a fost modificata cu succes! Id unic '+CAST(@IdCl AS VARCHAR(20)) + ' !');

	--DELETE
	DELETE FROM Clienti
	WHERE IdCl = @IdCl;
	SELECT * FROM Clienti
	PRINT(N'Clientul cu id-ul ' + CAST(@IdCl AS VARCHAR(100)) + ' a fost stearsa!');
END
GO

--Functie de validare Categorie
GO
CREATE OR ALTER FUNCTION Validare_Categorie(
	@IdC INT, --PK
	@NumeCategorie VARCHAR(50)
	)RETURNS INT AS BEGIN

	--Verificam daca mai exista vreun obiect cu acest id 
	DECLARE @idC_count INT;
	SELECT @idC_count =COUNT(*) FROM Categorie WHERE IdC = @IdC;

	IF @NumeCategorie IS NULL OR (@idC_count IS NOT NULL AND @idC_count > 0)
		RETURN 0

	RETURN 1
END
GO

GO
CREATE OR ALTER PROCEDURE CRUD_Categorie
	@IdC INT, 
	@NumeCategorie VARCHAR(50)
AS BEGIN
	DECLARE @validation_status INT;
	SELECT @validation_status = dbo.Validare_Categorie(@IdC,@NumeCategorie);
	IF (@validation_status = 0)
	BEGIN
		RAISERROR(N'Au fost introduse date incorecte', 16, 1);
		RETURN;
	END

	--CREATE = INSERT
	INSERT INTO Categorie(IdC,NumeCategorie)
		VALUES (@IdC,@NumeCategorie);
	SELECT * FROM Categorie
	PRINT(N'Categoria a fost creata cu succes! Folosim id-ul de categorie '+ CAST(@IdC AS VARCHAR(20))+' !');

	--READ = SELECT
	SELECT * FROM Categorie
	WHERE IdC = @IdC;
	PRINT(N'Categoria a fost printata cu succes cu id-ul ' + CAST(@IdC AS VARCHAR(100)) + ' !');

	--UPDATE
	UPDATE Categorie
	SET NumeCategorie = 'Update' + @NumeCategorie
	WHERE IdC = @IdC;
	SELECT * FROM Categorie
	PRINT(N'Categorie a fost modificata cu succes! Id unic '+CAST(@IdC AS VARCHAR(20)) + ' !');

	--DELETE
	DELETE FROM Categorie
	WHERE IdC = @IdC;
	SELECT * FROM Categorie
	PRINT(N'Categorie cu id-ul ' + CAST(@IdC AS VARCHAR(100)) + ' a fost stearsa!');
END
GO

--Functia de validare pentru Comenzi

GO
CREATE OR ALTER FUNCTION Validare_Comenzi(
	@IdC INT, --FK
	@IdCl INT, --FK
	@Suma INT,
	@Data DATE
	)RETURNS INT AS BEGIN 

	DECLARE @IdC_count INT;
	SELECT @IdC_count = COUNT(*) FROM Comenzi WHERE IdC = @IdC

	DECLARE @IdCl_count INT;
	SELECT @IdCl_count = COUNT(*) FROM Comenzi WHERE IdCl = @IdCl

	IF @Suma IS NULL OR @IdC_count = 0 OR @IdCl_count = 0
		RETURN 0;
	RETURN 1;
END
GO

GO 
CREATE OR ALTER PROCEDURE CRUD_Comenzi
	@IdC INT,
	@IdCl INT,
	@Suma INT,
	@Data DATE
AS BEGIN
	DECLARE @validation_status INT;
	SELECT @validation_status = dbo.Validare_Comenzi(@IdC,@IdCl,@Suma,@Data);
	IF (@validation_status = 0)
	BEGIN
		RAISERROR(N'Au fost introduse gresit datele', 16, 1);
		RETURN;
	END
	
	--CREATE = INSERT
	INSERT INTO Comenzi(IdC,IdCl,Suma,Data)
		VALUES (@IdC,@IdCl,@Suma,@Data);
	SELECT * FROM Comenzi
	PRINT(N'Conexiunea a fost creata cu succes!');

	--READ = SELECT
	SELECT * FROM Comenzi
	WHERE IdC = @IdC AND IdCl = @IdCl
	PRINT(N'Conexiunea a fost printata cu succes!');

	--UPDATE
	UPDATE Comenzi
	SET Suma = 100 + @Suma
	WHERE IdC = @IdC AND IdCl = @IdCl;
	SELECT * FROM Comenzi
	PRINT(N'Conexiunea a fost modificata cu succes!');

	--DELETE 
	DELETE FROM Comenzi
	WHERE IdC = @IdC AND IdCl = @IdCl
	SELECT * FROM Comenzi
	PRINT(N'Conexiune stearsa cu succes!');
END 
GO

--Functie de validare Depozit
GO
CREATE OR ALTER FUNCTION Validare_Depozit(
	@IdD INT, --PK
	@Nume VARCHAR(100),
	@Adresa VARCHAR(100),
	@Capacitate FLOAT
	)RETURNS INT AS BEGIN

	--Verificam daca mai exista vreun obiect cu acest id 
	DECLARE @idD_count INT;
	SELECT @idD_count =COUNT(*) FROM Depozit WHERE IdD = @IdD;

	IF @Nume IS NULL OR @Adresa IS NULL OR @Capacitate IS NULL OR (@idD_count IS NOT NULL AND @idD_count > 0)
		RETURN 0

	RETURN 1
END
GO

GO
CREATE OR ALTER PROCEDURE CRUD_Depozit
	@IdD INT,
	@Nume VARCHAR(100),
	@Adresa VARCHAR(100),
	@Capacitate FLOAT
AS BEGIN
	DECLARE @validation_status INT;
	SELECT @validation_status = dbo.Validare_Depozit(@IdD,@Nume,@Adresa,@Capacitate);
	IF (@validation_status = 0)
	BEGIN
		RAISERROR(N'Au fost introduse date incorecte', 16, 1);
		RETURN;
	END

	--CREATE = INSERT
	INSERT INTO Depozit(IdD,Nume,Adresa,Capacitate)
		VALUES (@IdD,@Nume,@Adresa,@Capacitate);
	SELECT * FROM Depozit
	PRINT(N'Depozitul a fost creata cu succes! Folosim id-ul de depozit '+ CAST(@IdD AS VARCHAR(20))+' !');

	--READ = SELECT
	SELECT * FROM Depozit
	WHERE IdD = @IdD;
	PRINT(N'Depozit a fost printata cu succes cu id-ul ' + CAST(@IdD AS VARCHAR(100)) + ' !');

	--UPDATE
	UPDATE Depozit
	SET Nume = 'Update' + @Nume
	WHERE IdD = @IdD;
	SELECT * FROM Depozit
	PRINT(N'Depozit a fost modificata cu succes! Id unic '+CAST(@IdD AS VARCHAR(20)) + ' !');

	--DELETE
	DELETE FROM Depozit
	WHERE IdD = @IdD;
	SELECT * FROM Depozit
	PRINT(N'Depozit cu id-ul ' + CAST(@IdD AS VARCHAR(100)) + ' a fost stearsa!');
END
GO

--Functie de validare Furnizor
GO
CREATE OR ALTER FUNCTION Validare_Furnizor(
	@IdF INT, --PK
	@NumeFurnizor VARCHAR(100),
	@Adresa VARCHAR(100)
	)RETURNS INT AS BEGIN

	--Verificam daca mai exista vreun obiect cu acest id 
	DECLARE @idF_count INT;
	SELECT @idF_count =COUNT(*) FROM Furnizori WHERE IdF = @IdF;

	IF @NumeFurnizor IS NULL OR @Adresa IS NULL OR (@idF_count IS NOT NULL AND @idF_count > 0)
		RETURN 0

	RETURN 1
END
GO

GO
CREATE OR ALTER PROCEDURE CRUD_Furnizor
	@IdF INT,
	@NumeFurnizor VARCHAR(100),
	@Adresa VARCHAR(100)
AS BEGIN
	DECLARE @validation_status INT;
	SELECT @validation_status = dbo.Validare_Furnizor(@IdF,@NumeFurnizor,@Adresa);
	IF (@validation_status = 0)
	BEGIN
		RAISERROR(N'Au fost introduse date incorecte', 16, 1);
		RETURN;
	END

	--CREATE = INSERT
	INSERT INTO Furnizori(IdF,NumeFurnizor,Adresa)
		VALUES (@IdF,@NumeFurnizor,@Adresa);
	SELECT * FROM Furnizori
	PRINT(N'Furnizorul a fost creata cu succes! Folosim id-ul de furnizor '+ CAST(@IdF AS VARCHAR(20))+' !');

	--READ = SELECT
	SELECT * FROM Furnizori
	WHERE IdF = @IdF;
	PRINT(N'Furnizorul a fost printata cu succes cu id-ul ' + CAST(@IdF AS VARCHAR(100)) + ' !');

	--UPDATE
	UPDATE Furnizori
	SET NumeFurnizor = 'Update' + @NumeFurnizor
	WHERE IdF = @IdF;
	SELECT * FROM Furnizori
	PRINT(N'FurNizorul a fost modificata cu succes! Id unic '+CAST(@IdF AS VARCHAR(20)) + ' !');

	--DELETE
	DELETE FROM Furnizori
	WHERE IdF = @IdF;
	SELECT * FROM Furnizori
	PRINT(N'Furnizorul cu id-ul ' + CAST(@IdF AS VARCHAR(100)) + ' a fost stearsa!');
END
GO

--VIEW

--Viziualizare Furnizori cu adresa in South-America
GO
CREATE OR ALTER VIEW VM_Furnizori AS
    SELECT IdF, Adresa 
    FROM Furnizori
    WHERE Adresa = 'South-America';
GO

--Vizualizari pentru comenzile grupate pe categorii cu media sumei > 2000 si < 3000
GO
CREATE OR ALTER VIEW VM_Comanda AS
	SELECT c.Idc AS Categorie, cat.NumeCategorie AS NumeCategorie, AVG(c.Suma) AS Medie_Suma 
	FROM Comenzi C 
	INNER JOIN Categorie cat ON c.IdC = cat.IdC 
	GROUP BY c.IdC, cat.NumeCategorie 
	HAVING AVG(c.Suma) > 2000 AND AVG(c.Suma) < 3000;
GO

--INDEX

IF EXISTS(SELECT name FROM sys.indexes WHERE name = N'idx_Comanda_IdC_Suma')
    DROP INDEX idx_Comanda_IdC_Suma ON Comenzi;
CREATE NONCLUSTERED INDEX idx_Comanda_IdC_Suma ON Comenzi(IdC, Suma);

SELECT * FROM VM_Comanda;

IF EXISTS (SELECT name FROM sys.indexes WHERE name = N'idx_Furnizori_Adrese')
	DROP INDEX idx_Furnizori_Adrese ON Furnizori;
CREATE NONCLUSTERED INDEX idx_Furnizori_Adrese ON Furnizori(Adresa,IdF);

SELECT * FROM VM_Furnizori

--Executia acestui CRUD pentru Clienti
EXEC CRUD_Clienti 10002, 'X','X@yahoo.ro','X','0764042377' 
--Executam acest CRUD pt Categorie
EXEC CRUD_Categorie 1, 'Schi'
--Executia acestui CRUD pentru Comenzi
EXEC CRUD_Comenzi 2,5,500,'2024-12-12'
--Executia acestui CRUD pt Depozit
EXEC CRUD_Depozit 6, 'Depozit de Vest', 'Paris', 4000
--Executia acestui CRUD pt Furnizor 
EXEC CRUD_Furnizor 11, 'Gucci', 'Italia'

SELECT * FROM Clienti ;
SELECT * FROM Comenzi;
SELECT * FROM Depozit;
SELECT * FROM Furnizori;

SELECT * FROM Comenzi WHERE IdC = 2;
SELECT * FROM Comenzi WHERE IdCl = 5;
