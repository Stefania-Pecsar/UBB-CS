USE Magazinsportiv

-- Vizualizează toate datele din tabelul Categorie
SELECT * FROM Categorie;

-- Vizualizează toate datele din tabelul Clienti
SELECT * FROM Clienti;

-- Vizualizează toate datele din tabelul Comenzi
SELECT * FROM Comenzi;

-- Vizualizează toate datele din tabelul Promotii
SELECT * FROM Promotii;

-- Vizualizează toate datele din tabelul Depozit
SELECT * FROM Depozit;

-- Vizualizează toate datele din tabelul Angajati
SELECT * FROM Angajati;

-- Vizualizează toate datele din tabelul Furnizori
SELECT * FROM Furnizori;

-- Vizualizează toate datele din tabelul Produse
SELECT * FROM Produse;

-- Vizualizează toate datele din tabelul Recenzii
SELECT * FROM Recenzii;

-- Vizualizează toate datele din tabelul Metoda_de_Plata
SELECT * FROM Metoda_de_Plata;



-- 1) Produsele impreuna cu furnizorii (WHERE)
SELECT p.Nume AS Produs, f.NumeFurnizor AS Furnizor, pr.Discount AS Promotii
FROM Produse p
INNER JOIN Furnizori f ON p.IdF = f.IdF
INNER JOIN Promotii pr ON p.IdPromotie = pr.IdPromotie
WHERE p.Brand = 'Nike' AND p.Stoc > 5;

--2) Comenzi realizate de clienti din "Hunedoara'(WHERE)
SELECT c.NumeClient, com.Suma, com.Data,AVG(r.Nota) AS Recenzie
FROM Comenzi com
INNER JOIN Clienti c ON com.IdCl = c.IdCl
INNER JOIN Recenzii r ON r.IdCl = c.IdCl
WHERE c.Adresa = 'Hunedoara'
GROUP BY c.NumeClient, com.Suma, com.Data
HAVING AVG(r.Nota) > 8;

--3)Angajati cu salariu peste 3000 grupat pe rol(WHERE,GROUP BY)
SELECT a.Rol,d.Nume AS NumeDepozit,f.NumeFurnizor,COUNT(*) AS Numar_Angajati
FROM Angajati a
INNER JOIN Depozit d ON a.IdD = d.IdD
INNER JOIN Produse p ON p.IdA = a.IdA
INNER JOIN Furnizori f ON p.IdF = f.IdF
WHERE a.Salariu > 3000
GROUP BY a.Rol, d.Nume, f.NumeFurnizor;

--4)Numărul de clienți care au plasat comenzi din fiecare categorie(GROUP BY,DISTINCT, m-n)
SELECT cat.NumeCategorie, COUNT(DISTINCT com.IdCl) AS Numar_Clienti
FROM Categorie cat
INNER JOIN Comenzi com ON cat.IdC = com.IdC
INNER JOIN Clienti cl ON cl.IdCl =com.IdCl
GROUP BY cat.NumeCategorie;

--5)Toate categoriile in care fiecare client a plasat comanda(DISTINCT,m-n)
SELECT DISTINCT c.NumeClient, cat.NumeCategorie
FROM Clienti c
INNER JOIN Comenzi com ON c.IdCl = com.IdCl
INNER JOIN Categorie cat ON com.IdC = cat.IdC;

--6)Suma totala a comenzilor plasate de fiecare client(GROUP BY)
SELECT c.NumeClient, SUM(com.Suma) AS Total_Comenzi, AVG(r.Nota) AS Media_recenzii
FROM Clienti c
INNER JOIN Comenzi com ON c.IdCl = com.IdCl
INNER JOIN Recenzii r ON r.IdCl=c.IdCl
GROUP BY c.NumeClient;

--7)Depozite și numărul de angajați din fiecare, dacă au mai mult de un angajat(GROUP BY, HAVING)
SELECT d.Nume AS Depozit, COUNT(a.IdA) AS Numar_Angajati, SUM(p.Pret) AS Suma_Preturi_Produse
FROM Depozit d
INNER JOIN Angajati a ON d.IdD = a.IdD
INNER JOIN Produse p ON p.IdA = a.IdA
GROUP BY d.Nume
HAVING COUNT(a.IdA) > 1;

--8)Furnizori cu produse unice(DISTINCT)
SELECT DISTINCT f.NumeFurnizor, p.Nume, a.NumeAngajati 
FROM Produse p
INNER JOIN Furnizori f ON p.IdF = f.IdF
INNER JOIN Angajati a ON p.IdA=a.IdA;

--9)Comenzi plasate in 2024(WHERE)
SELECT c.NumeClient, com.Data, r.Nota AS Recenzie
FROM Clienti c
INNER JOIN Comenzi com ON c.IdCl = com.IdCl
INNER JOIN Recenzii r ON com.IdC = r.IdCl
WHERE YEAR(com.Data) = 2024;

--10)Clientii care au facut comenzi peste 200, filtrati dupa mai mult de 500(WHERE,GROUP BY, HAVING)
SELECT c.NumeClient, COUNT(co.IdC) AS NumarComenzi, SUM(co.Suma) AS SumaTotala
FROM Clienti c
INNER JOIN Comenzi co ON c.IdCl = co.IdCl
WHERE co.Suma > 200  
GROUP BY c.NumeClient
HAVING SUM(co.Suma) > 500;
 

 --11)