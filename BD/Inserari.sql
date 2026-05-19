USE Magazinsportiv
GO

--Categorii
INSERT INTO Categorie(IdC,NumeCategorie)
VALUES (1,'Fitness'),
		(2,'Alergare'),
		(3,'Drumetie'),
		(4,'Alpinism'),
		(5,'Sporturi'),
		(6, 'Ciclism'),
        (7, 'Înot'),
        (8, 'Schi'),
        (9, 'Sporturi de echipă')

--Clienti
INSERT INTO Clienti(IdCl,NumeClient,Email,Adresa,Telefon)
VALUES (1,'Pecsar Stefania','stefaniapecsar@yahoo.ro','Hunedoara','0764042377'),
		(2,'Stroe Bogdan','bgdstr@yahoo.ro','Calan','0771184614'),
		(3,'Pecsar Tudor','tudorpecsar@yahoo.ro','Hunedoara','0764466360'),
		(4, 'Popescu Maria', 'maria.popescu@gmail.com', 'Sibiu', '0756781234'),
        (5, 'Ionescu Andrei', 'andrei.ionescu@yahoo.com', 'București', '0745567890'),
        (6, 'Georgescu Elena', 'elena.georgescu@hotmail.com', 'Brașov', '0765443321')

--Comenzi
INSERT INTO Comenzi(IdC,IdCl,Suma,Data)
VALUES (1,1,200,'2024-10-15'),
		(3,2,500,'2023-02-10'),
		(5,3,1000,'2024-02-11'),
		(2, 1, 250, '2024-10-16'),
        (4, 3, 300, '2024-10-20'),
        (6, 4, 450, '2024-10-18'),
        (7, 5, 600, '2024-10-22')

--Promotii
INSERT INTO Promotii(IdPromotie,Nume,Inceput,Sfarsit,Discount)
VALUES (1,'Craciun','2023-11-10 00:00:00', '2023-12-20 23:59:59',0.20),
		(2,'Aniversar','2023-06-17 05:00:00', '2023-06-20 23:59:59',0.30),
		(3,'Black Friday', '2023-11-25', '2023-11-27', 0.50),
		(4, 'Primăvară', '2024-03-01 00:00:00', '2024-03-31 23:59:59', 0.15),
        (5, 'Back to School', '2024-08-01 00:00:00', '2024-09-30 23:59:59', 0.25)

--Depozit
INSERT INTO Depozit(IdD,Nume,Adresa,Capacitate)
VALUES (1,'Depozit central','Cluj-Napoca',20000),
		(2,'Depozit regional','Hunedoara',1500),
		(3,'Depozit nord-estic','Tulcea',2500),
		(4, 'Depozit sudic', 'București', 3000),
        (5, 'Depozit de Est', 'Iași', 4000)

--Angajati
INSERT INTO Angajati(IdA,IdD,NumeAngajati,Rol,Salariu,DataNasterii,Telefon)
VALUES (1,3,'Oproi Denisa','Sefa',4999,'2004-03-05',0756423984),
		(2,1,'Negru Diana','Manager',4000,'2004-08-31',0745221546),
		(3,3,'Elena Stan', 'Consultant', 3000, '1985-07-20', '0744123456'),
		(4,2,'Emil Vladu','Depozit',3050,'1973-05-30','075694287'),
		(5, 4, 'Radu Sorin', 'Vânzător', 2800, '1990-05-15', '0755123456'),
        (6, 2, 'Marin Daniel', 'Asistent', 2900, '1992-11-23', '0766543210'),
        (7, 1, 'Dumitru Ioana', 'Manager Vânzări', 4500, '1988-04-10', '0744788999'),
		(8, 1, 'Radu Sorin', 'Vânzător', 2800, '1990-05-15', '0755123456'),
		(9, 2, 'Marin Daniel', 'Asistent', 2900, '1992-11-23', '0766543210'),
		(10, 3, 'Ionescu Raluca', 'Consultant', 3100, '1989-04-05', '0772233445'),
		(11, 1, 'Dumitru Victor', 'Securitate', 3200, '1985-06-15', '0745567890'),
		(12, 2, 'Popescu Ana', 'Vânzător', 3000, '1988-02-18', '0755112233'),
		(13, 3, 'Petrescu Cristian', 'Asistent Manager', 4000, '1986-03-27', '0744778899'),
		(14, 1, 'Georgescu Marius', 'Manager Logistic', 4500, '1987-11-30', '0778899000'),
		(15, 2, 'Dumitrescu Elena', 'Manager Vânzări', 4600, '1991-01-10', '0755246789'),
		(16, 3, 'Nicolescu Andreea', 'Contabil', 3700, '1984-09-22', '0772211333'),
		(17, 1, 'Stan Ion', 'Tehnician', 3300, '1993-07-14', '0751122334')

--Furnizori
INSERT INTO Furnizori (IdF,NumeFurnizor, Adresa) 
VALUES (1,'Nike', 'North-America'),
	   (2,'Adidas', 'North-America'),
	   (3,'Altra', 'North-America'),
       (4,'Under Armour', 'North-America'),
	   (5,'Puma', 'North-America'),
	   (6,'Patagonia', 'South-America'),
	   (7,'The North Face', 'North-America'),
	   (8, 'New Balance', 'North-America'),
       (9, 'Reebok', 'North-America'),
       (10, 'Salomon', 'Europe')

--Produse
INSERT INTO Produse(IdP,IdF,IdPromotie,IdA,Nume,Brand,Pret,Stoc,Descriere)
VALUES (1,1,1,1,'Tricou Sport','Nike',150.5,50,'Tricou antrenement'),
	   (2,5,3,2,'Pantofi','Puma',300.75,30,'Handball'),
	   (3, 1, 1, 1, 'Pantaloni Sport', 'Nike', 120.0, 40, 'Pantaloni pentru antrenament'),
       (4, 2, 3, 2, 'Adidași', 'Adidas', 250.5, 20, 'Adidași pentru alergare'),
       (5, 3, 4, 1, 'Căciulă', 'Patagonia', 40.0, 100, 'Căciulă călduroasă pentru iarnă'),
	   (6, 4, 1, 8, 'Rochie Sport', 'Under Armour', 180.5, 35, 'Rochie confortabilă pentru sport'),
	   (7, 6, 2, 9, 'Încălțări de alergare', 'Altra', 260.75, 25, 'Încălțări ușoare pentru alergători'),
       (8, 7, 3, 10, 'Pantaloni scurți', 'The North Face', 85.0, 40, 'Pantaloni scurți pentru vară'),
       (9, 5, 4, 11, 'Geacă de iarnă', 'Puma', 350.0, 20, 'Geacă călduroasă pentru iarnă'),
       (10, 1, 1, 12, 'Căciulă sport', 'Nike', 45.0, 60, 'Căciulă confortabilă pentru iarnă'),
       (11, 3, 2, 13, 'Tocator de sport', 'Adidas', 200.0, 15, 'Tocator pentru sportivi'),
       (12, 2, 4, 14, 'Bocanci de munte', 'Salomon', 500.0, 10, 'Bocanci pentru drumeții montane'),
       (13, 1, 3, 15, 'Minge de fotbal', 'Nike', 70.0, 50, 'Minge de fotbal de calitate'),
       (14, 4, 1, 16, 'Set de antrenament', 'Under Armour', 150.0, 5, 'Set complet pentru antrenamente'),
       (15, 5, 2, 17, 'Ciclism Mănuși', 'Puma', 30.0, 45, 'Mănuși pentru ciclism')

--Recenzii
INSERT INTO Recenzii(IdRecenzie,IdP,IdCl,Data_recenziei,Nota)
VALUES (1,1,3,'2024-10-22 10:00:00',10),
	   (2,1,1,'2023-10-23 14:30:30',9),
	   (3, 2, 4, '2024-10-25 11:00:00', 8),
       (4, 3, 5, '2024-10-26 09:30:00', 9),
	   (5, 4, 1, '2024-10-27 08:00:00', 9),
	   (6, 6, 3, '2024-10-28 12:30:00', 10)

--Metoda_de_Plata
INSERT INTO Metoda_de_Plata(IdMet,IdP,Nume_Metoda,Taxa_procesare)
VALUES (1,2,'Card',2.5),
	   (2,2,'Cash',0.0)