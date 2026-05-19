<<<<<<< Updated upstream
﻿===========================
PROIECT SGBD - LABORATOR 1
===========================

1. CONFIGURARE BAZĂ DE DATE
---------------------------
* Server utilizat: Microsoft SQL Server (SQLEXPRESS).
* Rulați mai întâi scriptul 'FirmaDeTransport.sql' pentru crearea structurii.
* Rulați apoi scriptul 'PopulareCuDate.sql' pentru datele de test.

2. CONFIGURARE CONEXIUNE
------------------------
* Deschideți fișierul 'DatabaseService.cs'.
* Modificați variabila 'ConnectionString' dacă instanța locală are alt nume.
  Exemplu: Server=DESKTOP-I0292P0\SQLEXPRESS;Database=FirmaDeTransportExtern;Integrated Security=True;TrustServerCertificate=true;

3. RULARE APLICAȚIE
-------------------
* Deschideți soluția în Visual Studio 2022.
* .NET WinForms
* Asigurați-vă că pachetul NuGet 'Microsoft.Data.SqlClient' este instalat.(necesare pentru comunicarea cu SQL Server)
* Apăsați F5 pentru pornire.


4. ARHITECTURĂ ȘI TEHNOLOGII
----------------------------
* Securitate: Toate operațiile CRUD folosesc interogări parametrizate (Prevenire SQL Injection)[cite: 35, 73].
* [Separarea Logicii: Clasa 'DatabaseService' gestionează exclusiv accesul la date, separat de codul UI din 'Form1.cs'.


5. FUNCȚIONALITĂȚI IMPLEMENTATE
-------------------------------
* Vizualizare Master-Detail (Firme -> Angajați). 
* Operații CRUD complete pe tabelul Angajați (Copil). 
* Refresh date și Validări (CNP 13 cifre, Salariu > 0).
=======
﻿===========================
PROIECT SGBD - LABORATOR 1
===========================

1. CONFIGURARE BAZĂ DE DATE
---------------------------
* Server utilizat: Microsoft SQL Server (SQLEXPRESS).
* Rulați mai întâi scriptul 'FirmaDeTransport.sql' pentru crearea structurii.
* Rulați apoi scriptul 'PopulareCuDate.sql' pentru datele de test.

2. CONFIGURARE CONEXIUNE
------------------------
* Deschideți fișierul 'DatabaseService.cs'.
* Modificați variabila 'ConnectionString' dacă instanța locală are alt nume.
  Exemplu: Server=DESKTOP-I0292P0\SQLEXPRESS;Database=FirmaDeTransportExtern;Integrated Security=True;TrustServerCertificate=true;

3. RULARE APLICAȚIE
-------------------
* Deschideți soluția în Visual Studio 2022.
* .NET WinForms
* Asigurați-vă că pachetul NuGet 'Microsoft.Data.SqlClient' este instalat.(necesare pentru comunicarea cu SQL Server)
* Apăsați F5 pentru pornire.


4. ARHITECTURĂ ȘI TEHNOLOGII
----------------------------
* Securitate: Toate operațiile CRUD folosesc interogări parametrizate (Prevenire SQL Injection)[cite: 35, 73].
* [Separarea Logicii: Clasa 'DatabaseService' gestionează exclusiv accesul la date, separat de codul UI din 'Form1.cs'.


5. FUNCȚIONALITĂȚI IMPLEMENTATE
-------------------------------
* Vizualizare Master-Detail (Firme -> Angajați). 
* Operații CRUD complete pe tabelul Angajați (Copil). 
* Refresh date și Validări (CNP 13 cifre, Salariu > 0).
>>>>>>> Stashed changes
* Dialog de confirmare la ștergere.