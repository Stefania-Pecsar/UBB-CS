<<<<<<< Updated upstream
﻿===========================
PROIECT SGBD - LABORATOR 2
===========================

## Rularea aplicației

1. Deschide soluția în Visual Studio.
2. Asigură‑te că proiectul se compilează.
3. Apasă `F5` pentru a rula aplicația.

## Interfață și demonstrații

Interfața conține butoane pentru fiecare scenariu. În partea dreaptă, un RichTextBox afișează pașii executați de tranzacții.

### 1. Dirty Read
- **Problemă**: Tranzacția A actualizează un salariu, dar nu face commit. Tranzacția B citește cu `ReadUncommitted` și vede valoarea necomisă.
- **Soluție**: Tranzacția B folosește `ReadCommitted` – nu mai vede datele necomise.

### 2. Non‑repeatable Read
- **Problemă**: Tranzacția A citește același rând de două ori cu `ReadCommitted`. Între citiri, Tranzacția B modifică rândul și face commit. Cele două citiri diferă.
- **Soluție**: Tranzacția A folosește `RepeatableRead` – blochează rândul citit și nu permite modificări până la finalul tranzacției.

### 3. Phantom Read
- **Problemă**: Tranzacția A numără înregistrările cu `functie = 'TestPhantom'` de două ori cu `RepeatableRead`. Între numărări, Tranzacția B inserează o înregistrare nouă care îndeplinește condiția. Cele două numărări diferă.
- **Soluție**: Tranzacția A folosește `Serializable` – blochează întregul interval, prevenind inserarea.

### 4. Lost Update
- **Problemă**: Două tranzacții citesc același salariu (5000), fiecare își calculează o nouă valoare (A: +1000 → 6000, B: +500 → 5500). Ambele actualizează cu `ReadCommitted`, fără condiții suplimentare. Ultima actualizare (A) suprascrie prima, pierzând actualizarea lui B.
- **Soluție**: Abordare optimistă – la actualizare se verifică dacă valoarea citită nu s‑a schimbat (`WHERE salar = @oldSalary`). Astfel, una dintre tranzacții eșuează și face rollback, iar cealaltă reușește. Se evită deadlock‑ul și pierderea.

### 5. Deadlock
- **Problemă**: Două tranzacții blochează resurse în ordine inversă. Tranzacția A blochează angajatul 1, apoi încearcă să blocheze angajatul 2. Tranzacția B blochează angajatul 2, apoi încearcă să blocheze angajatul 1. Rezultă deadlock; SQL Server alege o victimă și o oprește.
- **Soluție**: Se impune aceeași ordine de acces în ambele tranzacții (prin parametrul `solved`). Deadlock‑ul dispare.

### 6. Test performanță batch (5000 de inserări)
Se măsoară timpul pentru trei strategii, fiecare rulată de 3 ori:
- **Auto‑commit**: fiecare `INSERT` se execută într‑o tranzacție implicită.
- **Commit în loturi**: tranzacție care face commit la fiecare 100 de inserări.
- **Tranzacție unică**: o singură tranzacție pentru toate inserările.

La final se afișează mediile. Rezultatele sunt utile pentru a observa diferențele de performanță între abordări.

## Posibile probleme

- **Eroare de conexiune**: Verifică șirul de conexiune și asigură‑te că baza de date există.
- **Deadlock în Lost Update (soluție)**: În codul final am folosit metoda  (cu `WHERE salar = @oldSalary`) care elimină deadlock‑ul. 

## Structura proiectului

- `Form1.cs` – codul principal cu toate demonstrațiile.
- `Form1.Designer.cs` – definiția controalelor (generată automat).
- `Program.cs` – punctul de intrare.
- `PopulareCuDate.sql` – script pentru crearea tabelelor și datelor de test.
=======
﻿===========================
PROIECT SGBD - LABORATOR 2
===========================

## Rularea aplicației

1. Deschide soluția în Visual Studio.
2. Asigură‑te că proiectul se compilează.
3. Apasă `F5` pentru a rula aplicația.

## Interfață și demonstrații

Interfața conține butoane pentru fiecare scenariu. În partea dreaptă, un RichTextBox afișează pașii executați de tranzacții.

### 1. Dirty Read
- **Problemă**: Tranzacția A actualizează un salariu, dar nu face commit. Tranzacția B citește cu `ReadUncommitted` și vede valoarea necomisă.
- **Soluție**: Tranzacția B folosește `ReadCommitted` – nu mai vede datele necomise.

### 2. Non‑repeatable Read
- **Problemă**: Tranzacția A citește același rând de două ori cu `ReadCommitted`. Între citiri, Tranzacția B modifică rândul și face commit. Cele două citiri diferă.
- **Soluție**: Tranzacția A folosește `RepeatableRead` – blochează rândul citit și nu permite modificări până la finalul tranzacției.

### 3. Phantom Read
- **Problemă**: Tranzacția A numără înregistrările cu `functie = 'TestPhantom'` de două ori cu `RepeatableRead`. Între numărări, Tranzacția B inserează o înregistrare nouă care îndeplinește condiția. Cele două numărări diferă.
- **Soluție**: Tranzacția A folosește `Serializable` – blochează întregul interval, prevenind inserarea.

### 4. Lost Update
- **Problemă**: Două tranzacții citesc același salariu (5000), fiecare își calculează o nouă valoare (A: +1000 → 6000, B: +500 → 5500). Ambele actualizează cu `ReadCommitted`, fără condiții suplimentare. Ultima actualizare (A) suprascrie prima, pierzând actualizarea lui B.
- **Soluție**: Abordare optimistă – la actualizare se verifică dacă valoarea citită nu s‑a schimbat (`WHERE salar = @oldSalary`). Astfel, una dintre tranzacții eșuează și face rollback, iar cealaltă reușește. Se evită deadlock‑ul și pierderea.

### 5. Deadlock
- **Problemă**: Două tranzacții blochează resurse în ordine inversă. Tranzacția A blochează angajatul 1, apoi încearcă să blocheze angajatul 2. Tranzacția B blochează angajatul 2, apoi încearcă să blocheze angajatul 1. Rezultă deadlock; SQL Server alege o victimă și o oprește.
- **Soluție**: Se impune aceeași ordine de acces în ambele tranzacții (prin parametrul `solved`). Deadlock‑ul dispare.

### 6. Test performanță batch (5000 de inserări)
Se măsoară timpul pentru trei strategii, fiecare rulată de 3 ori:
- **Auto‑commit**: fiecare `INSERT` se execută într‑o tranzacție implicită.
- **Commit în loturi**: tranzacție care face commit la fiecare 100 de inserări.
- **Tranzacție unică**: o singură tranzacție pentru toate inserările.

La final se afișează mediile. Rezultatele sunt utile pentru a observa diferențele de performanță între abordări.

## Posibile probleme

- **Eroare de conexiune**: Verifică șirul de conexiune și asigură‑te că baza de date există.
- **Deadlock în Lost Update (soluție)**: În codul final am folosit metoda  (cu `WHERE salar = @oldSalary`) care elimină deadlock‑ul. 

## Structura proiectului

- `Form1.cs` – codul principal cu toate demonstrațiile.
- `Form1.Designer.cs` – definiția controalelor (generată automat).
- `Program.cs` – punctul de intrare.
- `PopulareCuDate.sql` – script pentru crearea tabelelor și datelor de test.
>>>>>>> Stashed changes
