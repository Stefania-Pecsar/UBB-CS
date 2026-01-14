USE Magazinsportiv

--Procedura de testare pentru toate View-urile 
--(adaugam in tabelul TestRunView cat dureaza selectul pentru fiecare View)
GO
CREATE OR ALTER PROCEDURE testRunViewProc AS
BEGIN
	SET NOCOUNT ON;
	DECLARE @start DATETIME;
	DECLARE @end DATETIME;
	DECLARE @view INT;

	SELECT @view = ViewID FROM Views WHERE Name = 'View_Client';
	IF @view IS NULL
	BEGIN
		PRINT 'View_Categorie not found in Views table';
		RETURN;
	END
	SET @start = SYSDATETIME();
	SELECT * FROM View_Categorie;
	SET @end = SYSDATETIME();
	PRINT('View_Categorie test time: ' + CAST(DATEDIFF(ms,@start,@end) AS VARCHAR) + ' ms')
	INSERT INTO TestRuns(Description, StartAt,EndAt) VALUES
			('View_Categorie Test ',@start,@end);
	INSERT INTO TestRunViews(TestRunID,ViewID,StartAt,EndAt) VALUES
			(@@IDENTITY,@view,@start,@end);
	SET @view = @view + 1

	SELECT @view = ViewID FROM Views WHERE Name = 'View_CategorieClienti';
	SET @start = SYSDATETIME();
	SELECT * FROM View_CategorieClienti;
	SET @end = SYSDATETIME();
	PRINT ('View_CategorieClient test time: ' + CAST(DATEDIFF(ms,@start,@end) AS VARCHAR) + ' ms')
	INSERT INTO TestRuns(Description,StartAt,EndAt) VALUES
			('View_CategorieClient Test ',@start,@end);
	INSERT INTO TestRunViews(TestRunID,ViewID,StartAt,EndAt) values 
			(@@IDENTITY,@view,@start,@end);
	SET @view = @view + 1

	SELECT @view = ViewID FROM Views WHERE Name = 'View_MagazinCategorieClienti';
	SET @start = SYSDATETIME();
	SELECT * FROM View_MagazinCategorieClienti;
	SET @end = SYSDATETIME();
	PRINT('View_Comenzi_Client_Suma test time: ' + CAST(DATEDIFF(ms,@start,@end) AS VARCHAR) + ' ms')
	INSERT INTO TestRuns(Description,StartAt,EndAt) VALUES
			('View_Comenzi_Client_Suma Test ',@start,@end);
	INSERT INTO TestRunViews(TestRunID,ViewID,StartAt,EndAt) VALUES
			(@@IDENTITY,@view,@start,@end)
END

--Insertul pentru Categorie
GO
CREATE OR ALTER PROC insertCategorie AS
BEGIN
		DECLARE @rows INT = (SELECT TOP 1 TT.NoOfRows
		FROM TestTables TT INNER JOIN Tests T ON TT.TestID=T.TestID
		WHERE T.Name = 'insertCategorie');

		DECLARE @current INT = 1;
		DECLARE @id INT=11;
		WHILE @current <= @rows
		BEGIN
			INSERT INTO Categorie(IdC, NumeCategorie)  VALUES
			( @id, 'numeCateg')
			SET @id = @id + 1
			SET @current = @current + 1
		END
END
GO
CREATE OR ALTER PROCEDURE INSERT_CATEGORIE AS
BEGIN
	SET NOCOUNT ON;
	DECLARE @start DATETIME;
	DECLARE @end DATETIME;
	DECLARE @table INT;
		
	SELECT @table = TableID FROM Tables WHERE Name='Categorie';
	SET @start = SYSDATETIME();
	EXEC insertCategorie;
	SET @end = SYSDATETIME();
	PRINT('insertCategorie test time: ' + CAST(DATEDIFF(ms, @start, @end) AS VARCHAR) + ' ms')
	INSERT INTO TestRuns(Description, StartAt, EndAt) VALUES
		('insertCategorie Test', @start, @end)
	INSERT INTO TestRunTables(TestRunID, TableID, StartAt, EndAt) VALUES
		(@@IDENTITY, @table, @start, @end);
END

--Insertul pentru Clienti
GO
CREATE OR ALTER PROC insertClienti AS
BEGIN
	DECLARE @rows INT = (SELECT TOP 1 TT.NoOfRows
		FROM TestTables TT INNER JOIN Tests T ON TT.TestID=T.TestID
		WHERE T.Name = 'insertClienti');

	DECLARE @current INT = 1;
	DECLARE @id INT = 1;
	WHILE @current <= @rows
	BEGIN
		IF @id = 5229
		BEGIN
			SET @id = @id + 1
		END
		INSERT INTO Clienti(IdCl, NumeClient, Email, Adresa, Telefon) VALUES
		(CAST(@id AS VARCHAR), 'nume', 'email', 'adresa', 'telefon');
		SET @current = @current + 1
		SET @id = @id + 1
	END
END
GO
CREATE OR ALTER PROCEDURE INSERT_CLIENTI AS
BEGIN
	SET NOCOUNT ON;
	DECLARE @start DATETIME;
	DECLARE @end DATETIME;
	DECLARE @table INT;

	SELECT @table = TableID FROM Tables WHERE Name = 'Clienti';
	SET @start = SYSDATETIME();
	EXEC insertClienti;
	SET @end = SYSDATETIME();
	PRINT('insertClienti test time: ' + CAST(DATEDIFF(ms, @start, @end) AS VARCHAR) + ' ms')
	INSERT INTO TestRuns(Description, StartAt, EndAt) VALUES
		('insertClienti Test', @start, @end)
	INSERT INTO TestRunTables(TestRunID, TableID, StartAt, EndAt) VALUES
		(@@IDENTITY, @table, @start, @end);
END

--Inserare pentru Comenzi
GO
CREATE OR ALTER PROC insertComenzi AS
BEGIN
	DECLARE @rows INT = (SELECT TOP 1 TT.NoOfRows
		FROM TestTables TT INNER JOIN Tests T ON TT.TestID=T.TestID
		WHERE T.Name = 'insertComenzi');

		DECLARE @current INT = 1;
		DECLARE @idCO INT = 16;
		DECLARE @idCL INT = 11;

		WHILE @current <= @rows
		BEGIN
			INSERT INTO Comenzi(IdC, IdCl, Suma, Data) VALUES
			(@idCO, @idCL, (100 * @current), '2024-12-01');
			SET @idCO = @idCO + 1
			SET @idCL = @idCL + 1
			SET @current = @current + 1
		END
END
GO
CREATE OR ALTER PROCEDURE INSERT_COMENZI AS
BEGIN
	SET NOCOUNT ON;
	DECLARE @start DATETIME;
	DECLARE @end DATETIME;
	DECLARE @table INT;

	SELECT @table = TableID FROM Tables WHERE Name='Comenzi';
	SET @start = SYSDATETIME();
	EXEC insertComenzi;
	SET @end = SYSDATETIME();
	PRINT('insertComenzi test time: ' + CAST(DATEDIFF(ms, @start, @end) AS VARCHAR) + ' ms')
	INSERT INTO TestRuns(Description, StartAt, EndAt) VALUES
		('insertComenzi Test', @start, @end)
	INSERT INTO TestRunTables(TestRunID, TableID, StartAt, EndAt) VALUES
		(@@IDENTITY, @table, @start, @end);
END

--Delete pe Comanda
GO
CREATE OR ALTER PROCEDURE deleteComanda AS
BEGIN
	DECLARE @rows INT = (SELECT TOP 1 TT.NoOfRows
		FROM TestTables TT INNER JOIN Tests T ON TT.TestID=T.TestID
		WHERE T.Name = 'deleteComanda');

	DECLARE @current INT = 1;
		DECLARE @idCO INT = 16;
		DECLARE @idCL INT = 11;
		WHILE @current <= @rows
		BEGIN
			DELETE FROM Comenzi WHERE IdCl = @idCL AND IdC = @idCO;
			SET @idCO = @idCO + 1
			SET @idCL = @idCL + 1
			SET @current = @current + 1
		END
END

GO
CREATE OR ALTER PROCEDURE DELETE_COMANDA AS
BEGIN
	SET NOCOUNT ON;
	DECLARE @start DATETIME;
	DECLARE @end DATETIME;
	DECLARE @table INT;

	SELECT @table = TableID FROM Tables WHERE Name = 'Comenzi';
	SET @start = SYSDATETIME();
	EXEC deleteComanda;
	SET @end = SYSDATETIME();
	PRINT('deleteComanda test time: ' + CAST(DATEDIFF(ms, @start, @end) AS VARCHAR) + ' ms');
	INSERT INTO TestRuns(Description, StartAt, EndAt) VALUES
		('deleteComanda Test', @start, @end)
	INSERT INTO TestRunTables(TestRunID, TableID, StartAt, EndAt) VALUES
		(@@IDENTITY, @table, @start, @end)
END

--Delete pe Clienti
GO
CREATE OR ALTER PROCEDURE deleteClienti AS
BEGIN
	
	DECLARE @rows INT = (SELECT TOP 1 TT.NoOfRows
		FROM TestTables TT INNER JOIN Tests T ON TT.TestID=T.TestID
		WHERE T.Name = 'deleteClienti');

	DECLARE @current INT = 1;
	DECLARE @id INT = 11;
	WHILE @current <= @rows
	BEGIN
		DELETE FROM Clienti WHERE IdCl = @id;
		SET @id = @id + 1
		SET @current = @current + 1
	END
END
GO
CREATE OR ALTER PROCEDURE DELETE_CLIENT AS
BEGIN
	SET NOCOUNT ON;
	DECLARE @start DATETIME;
	DECLARE @end DATETIME;
	DECLARE @table INT;

	SELECT @table = TableID FROM Tables WHERE Name = 'Clienti';
	SET @start = SYSDATETIME();
	EXEC deleteClienti;
	SET @end = SYSDATETIME();
	PRINT('deleteClienti test time: ' + CAST(DATEDIFF(ms, @start, @end) AS VARCHAR) + ' ms');
	INSERT INTO TestRuns(Description, StartAt, EndAt) VALUES
		('deleteClienti Test', @start, @end)
	INSERT INTO TestRunTables(TestRunID, TableID, StartAt, EndAt) VALUES
		(@@IDENTITY, @table, @start, @end)
END

--Delete pe Categorie
GO
CREATE OR ALTER PROCEDURE deleteCategorie AS
BEGIN

	DECLARE @rows INT = (SELECT TOP 1 TT.NoOfRows
		FROM TestTables TT INNER JOIN Tests T ON TT.TestID=T.TestID
		WHERE T.Name = 'deleteCategorie');

	DECLARE @current INT = 1;
	DECLARE @IdC INT = 1;
	WHILE @current <= @rows
	BEGIN
		DELETE FROM Categorie WHERE IdC = @idC;
        SET @idC = @idC + 1;
        SET @current = @current + 1;
    END
END

GO
CREATE OR ALTER PROCEDURE DELETE_CATEGORIE AS
BEGIN
	SET NOCOUNT ON;
	DECLARE @start DATETIME;
	DECLARE @end DATETIME;
	DECLARE @table INT;

	SELECT @table = TableID FROM Tables WHERE Name = 'Categorie';
	SET @start = SYSDATETIME();
	EXEC deleteCategorie;
	SET @end = SYSDATETIME();
	PRINT('deleteCategorie test time: ' + CAST(DATEDIFF(ms, @start, @end) AS VARCHAR) + ' ms');
	INSERT INTO TestRuns(Description, StartAt, EndAt) VALUES
		('deleteCategorie Test', @start, @end)
	INSERT INTO TestRunTables(TestRunID, TableID, StartAt, EndAt) VALUES
		(@@IDENTITY, @table, @start, @end)
END


--Main ul (facut de mine ca sa aiba sens acel Position pentru mine :) )
GO
CREATE OR ALTER PROCEDURE main AS
BEGIN
	DECLARE @TestID INT, @TableID INT, @NoOfRows INT, @Position INT;
	SELECT TOP 1 @TestID = TestID, @TableID = TableID, @NoOfRows = NoOfRows, @Position = Position
	FROM TestTables
	ORDER BY Position;
	WHILE @@ROWCOUNT > 0
	BEGIN
		-- Apelează procedura stocată aici
		--EXEC NumeleProcedurii @TestID, @TableID, @NoOfRows, @Position;
		IF @Position = 1
		BEGIN
			EXEC INSERT_CATEGORIE;
		END

		IF @Position = 2
		BEGIN
			EXEC INSERT_CLIENTI;
		END

		IF @Position = 3
		BEGIN
			EXEC INSERT_COMENZI;
			EXEC testRunViewProc;
		END

		IF @Position = 4
		BEGIN
			EXEC DELETE_COMANDA;
		END

		IF @Position = 5
		BEGIN
			EXEC DELETE_CLIENT;
		END

		IF @Position = 6
		BEGIN
			EXEC DELETE_CATEGORIE;
		END

		SELECT TOP 1 @TestID = TestID, @TableID = TableID, @NoOfRows = NoOfRows, @Position = Position
		FROM TestTables
		WHERE Position > @Position
		ORDER BY Position;
	END;
END


EXEC main

SELECT * FROM TestRuns;
DELETE FROM TestRuns;

SELECT * FROM Clienti;
SELECT * FROM Comenzi;
SELECT * FROM Categorie;
