using Microsoft.Data.SqlClient;
using System;
using System.Diagnostics;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace SGBD_Lab2
{
    public partial class Form1 : Form
    {
        private string connectionString = "Server=DESKTOP-I0292P0\\SQLEXPRESS;Database=FirmaDeTransportExtern;Integrated Security=True;TrustServerCertificate=true";

        // Folosim 2 angajati din DB pentru testele de Deadlock
        private string cnpTest1 = "1980101456789"; // Popescu Ana
        private string cnpTest2 = "1970523678910"; // Ionescu Andrei

        public Form1()
        {
            InitializeComponent();
        }

        private void LogMessage(string message)
        {
            if (rtbLogs.InvokeRequired)
            {
                rtbLogs.Invoke(new Action(() => rtbLogs.AppendText(message + Environment.NewLine)));
            }
            else
            {
                rtbLogs.AppendText(message + Environment.NewLine);
            }
        }

        // ==========================================================
        // DEMONSTRATIE 1: DIRTY READ
        // ==========================================================

        private async void btnDirtyReadProblem_Click(object sender, EventArgs e)
        {
            rtbLogs.Clear();
            LogMessage("=== START DEMO DIRTY READ (Apare Problema) ===");

            Task taskA = Task.Run(() => RunTransactionA());
            Task taskB = Task.Run(() => RunTransactionB(System.Data.IsolationLevel.ReadUncommitted));

            await Task.WhenAll(taskA, taskB);
            LogMessage("=== END DEMO ===" + Environment.NewLine);
        }

        private async void btnDirtyReadSolved_Click(object sender, EventArgs e)
        {
            rtbLogs.Clear();
            LogMessage("=== START DEMO DIRTY READ (Prevenita) ===");

            Task taskA = Task.Run(() => RunTransactionA());
            Task taskB = Task.Run(() => RunTransactionB(System.Data.IsolationLevel.ReadCommitted));

            await Task.WhenAll(taskA, taskB);
            LogMessage("=== END DEMO ===" + Environment.NewLine);
        }

        private void RunTransactionA()
        {
            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();
                using (SqlTransaction tx = conn.BeginTransaction())
                {
                    LogMessage("Tranzactia A: BEGIN TRANSACTION");
                    try
                    {
                        using (SqlCommand cmd = new SqlCommand("UPDATE Angajati SET salar = 10000 WHERE cnp = @cnp", conn, tx))
                        {
                            cmd.Parameters.AddWithValue("@cnp", cnpTest1);
                            cmd.ExecuteNonQuery();
                            LogMessage("Tranzactia A: Salariu actualizat la 10000 (ne-comis)");
                        }

                        Task.Delay(3000).Wait();

                        tx.Rollback();
                        LogMessage("Tranzactia A: ROLLBACK efectuat! Salariul a revenit la normal.");
                    }
                    catch (Exception ex)
                    {
                        tx.Rollback();
                        LogMessage("Eroare Tx A: " + ex.Message);
                    }
                }
            }
        }

        private void RunTransactionB(System.Data.IsolationLevel isolationLevel)
        {
            Task.Delay(1000).Wait();

            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();
                using (SqlTransaction tx = conn.BeginTransaction(isolationLevel))
                {
                    LogMessage($"Tranzactia B: BEGIN TRANSACTION ({isolationLevel})");
                    try
                    {
                        using (SqlCommand cmd = new SqlCommand("SELECT salar FROM Angajati WHERE cnp = @cnp", conn, tx))
                        {
                            cmd.Parameters.AddWithValue("@cnp", cnpTest1);
                            var result = cmd.ExecuteScalar();
                            LogMessage($"Tranzactia B: Valoarea salariului citita este {result}");
                        }
                        tx.Commit();
                        LogMessage("Tranzactia B: COMMIT");
                    }
                    catch (Exception ex)
                    {
                        tx.Rollback();
                        LogMessage("Eroare Tx B: " + ex.Message);
                    }
                }
            }
        }

        // ==========================================================
        // DEMONSTRATIE 2: NON-REPEATABLE READ
        // ==========================================================

        private async void btnNonRepeatableProblem_Click(object sender, EventArgs e)
        {
            rtbLogs.Clear();
            LogMessage("=== START DEMO NON-REPEATABLE READ (Apare Problema) ===");

            Task taskA = Task.Run(() => RunNonRepeatableTransactionA(System.Data.IsolationLevel.ReadCommitted));
            Task taskB = Task.Run(() => RunNonRepeatableTransactionB());

            await Task.WhenAll(taskA, taskB);
            LogMessage("=== END DEMO ===" + Environment.NewLine);
        }

        private async void btnNonRepeatableSolved_Click(object sender, EventArgs e)
        {
            rtbLogs.Clear();
            LogMessage("=== START DEMO NON-REPEATABLE READ (Prevenita) ===");

            Task taskA = Task.Run(() => RunNonRepeatableTransactionA(System.Data.IsolationLevel.RepeatableRead));
            Task taskB = Task.Run(() => RunNonRepeatableTransactionB());

            await Task.WhenAll(taskA, taskB);
            LogMessage("=== END DEMO ===" + Environment.NewLine);
        }

        private void RunNonRepeatableTransactionA(System.Data.IsolationLevel isolationLevel)
        {
            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();
                using (SqlTransaction tx = conn.BeginTransaction(isolationLevel))
                {
                    LogMessage($"Tranzactia A: BEGIN TRANSACTION ({isolationLevel})");
                    try
                    {
                        using (SqlCommand cmd = new SqlCommand("SELECT salar FROM Angajati WHERE cnp = @cnp", conn, tx))
                        {
                            cmd.Parameters.AddWithValue("@cnp", cnpTest1);
                            var result1 = cmd.ExecuteScalar();
                            LogMessage($"Tranzactia A: Prima citire a returnat salariul: {result1}");
                        }

                        Task.Delay(3000).Wait();

                        using (SqlCommand cmd = new SqlCommand("SELECT salar FROM Angajati WHERE cnp = @cnp", conn, tx))
                        {
                            cmd.Parameters.AddWithValue("@cnp", cnpTest1);
                            var result2 = cmd.ExecuteScalar();
                            LogMessage($"Tranzactia A: A doua citire a returnat salariul: {result2}");
                        }

                        tx.Commit();
                        LogMessage("Tranzactia A: COMMIT");
                    }
                    catch (Exception ex)
                    {
                        tx.Rollback();
                        LogMessage("Eroare Tx A: " + ex.Message);
                    }
                }
            }
        }

        private void RunNonRepeatableTransactionB()
        {
            Task.Delay(1000).Wait();

            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();
                using (SqlTransaction tx = conn.BeginTransaction())
                {
                    LogMessage("Tranzactia B: BEGIN TRANSACTION");
                    try
                    {
                        using (SqlCommand cmd = new SqlCommand("UPDATE Angajati SET salar = salar + 100 WHERE cnp = @cnp", conn, tx))
                        {
                            cmd.Parameters.AddWithValue("@cnp", cnpTest1);
                            cmd.ExecuteNonQuery();
                            LogMessage("Tranzactia B: Salariu actualizat (+100)");
                        }

                        tx.Commit();
                        LogMessage("Tranzactia B: COMMIT efectuat");
                    }
                    catch (Exception ex)
                    {
                        tx.Rollback();
                        LogMessage("Eroare Tx B (sau blocata): " + ex.Message);
                    }
                }
            }
        }

        // ==========================================================
        // DEMONSTRATIE 3: PHANTOM READ
        // ==========================================================

        private void CleanUpPhantomData()
        {
            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();
                using (SqlCommand cmd = new SqlCommand("DELETE FROM Angajati WHERE functie = 'TestPhantom'", conn))
                {
                    cmd.ExecuteNonQuery();
                }
            }
        }

        private async void btnPhantomProblem_Click(object sender, EventArgs e)
        {
            CleanUpPhantomData();
            rtbLogs.Clear();
            LogMessage("=== START DEMO PHANTOM READ (Apare Problema) ===");

            Task taskA = Task.Run(() => RunPhantomTransactionA(System.Data.IsolationLevel.RepeatableRead));
            Task taskB = Task.Run(() => RunPhantomTransactionB());

            await Task.WhenAll(taskA, taskB);
            LogMessage("=== END DEMO ===" + Environment.NewLine);
        }

        private async void btnPhantomSolved_Click(object sender, EventArgs e)
        {
            CleanUpPhantomData();
            rtbLogs.Clear();
            LogMessage("=== START DEMO PHANTOM READ (Prevenita) ===");

            Task taskA = Task.Run(() => RunPhantomTransactionA(System.Data.IsolationLevel.Serializable));
            Task taskB = Task.Run(() => RunPhantomTransactionB());

            await Task.WhenAll(taskA, taskB);
            LogMessage("=== END DEMO ===" + Environment.NewLine);
        }

        private void RunPhantomTransactionA(System.Data.IsolationLevel isolationLevel)
        {
            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();
                using (SqlTransaction tx = conn.BeginTransaction(isolationLevel))
                {
                    LogMessage($"Tranzactia A: BEGIN TRANSACTION ({isolationLevel})");
                    try
                    {
                        string countQuery = "SELECT COUNT(*) FROM Angajati WHERE functie = 'TestPhantom'";
                        using (SqlCommand cmd = new SqlCommand(countQuery, conn, tx))
                        {
                            var count1 = cmd.ExecuteScalar();
                            LogMessage($"Tranzactia A: Prima numaratoare (TestPhantom): {count1}");
                        }

                        Task.Delay(3000).Wait();

                        using (SqlCommand cmd = new SqlCommand(countQuery, conn, tx))
                        {
                            var count2 = cmd.ExecuteScalar();
                            LogMessage($"Tranzactia A: A doua numaratoare (TestPhantom): {count2}");
                        }

                        tx.Commit();
                        LogMessage("Tranzactia A: COMMIT");
                    }
                    catch (Exception ex)
                    {
                        tx.Rollback();
                        LogMessage("Eroare Tx A: " + ex.Message);
                    }
                }
            }
        }

        private void RunPhantomTransactionB()
        {
            Task.Delay(1000).Wait();

            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();
                using (SqlTransaction tx = conn.BeginTransaction())
                {
                    LogMessage("Tranzactia B: BEGIN TRANSACTION");
                    try
                    {
                        string cnpRandom = DateTime.Now.Ticks.ToString().Substring(0, 13);
                        string insertQuery = "INSERT INTO Angajati (cnp, caen, nume, prenume, functie, salar, bonusuri) VALUES (@cnp, '5229', 'Fantoma', 'Test', 'TestPhantom', 1000, 0)";

                        using (SqlCommand cmd = new SqlCommand(insertQuery, conn, tx))
                        {
                            cmd.Parameters.AddWithValue("@cnp", cnpRandom);
                            cmd.ExecuteNonQuery();
                            LogMessage("Tranzactia B: Angajat nou inserat (Fantoma)");
                        }

                        tx.Commit();
                        LogMessage("Tranzactia B: COMMIT efectuat");
                    }
                    catch (Exception ex)
                    {
                        tx.Rollback();
                        LogMessage("Eroare Tx B (sau a fost blocata): " + ex.Message);
                    }
                }
            }
        }

        // // ==========================================================
        // DEMONSTRATIE 4: LOST UPDATE
        // ==========================================================

        // PROBLEMA: Lost update care apare
        private async void btnLostUpdateProblem_Click(object sender, EventArgs e)
        {
            rtbLogs.Clear();
            LogMessage("=== START DEMO LOST UPDATE (Apare Problema) ===");
            ResetSalaryTo(cnpTest1, 5000);

            Task taskA = Task.Run(() => RunLostUpdateProblemA(System.Data.IsolationLevel.ReadCommitted));
            Task taskB = Task.Run(() => RunLostUpdateProblemB(System.Data.IsolationLevel.ReadCommitted));

            await Task.WhenAll(taskA, taskB);

            double finalSalary = GetCurrentSalary(cnpTest1);
            LogMessage($"=== END DEMO === Salariul final in BD: {finalSalary}");
        }

        // SOLUTIE: Lost update prevenita prin actualizare condiționată 
        private async void btnLostUpdateSolved_Click(object sender, EventArgs e)
        {
            rtbLogs.Clear();
            LogMessage("=== START DEMO LOST UPDATE (Prevenita) ===");
            ResetSalaryTo(cnpTest1, 5000);

            Task taskA = Task.Run(() => RunLostUpdateSolvedA());
            Task taskB = Task.Run(() => RunLostUpdateSolvedB());

            await Task.WhenAll(taskA, taskB);

            double finalSalary = GetCurrentSalary(cnpTest1);
            LogMessage($"=== END DEMO === Salariul final in BD: {finalSalary}");
        }

        // Metode pentru problema 
        private void RunLostUpdateProblemA(System.Data.IsolationLevel isolationLevel)
        {
            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();
                using (SqlTransaction tx = conn.BeginTransaction(isolationLevel))
                {
                    LogMessage($"Tranzactia A: BEGIN TRANSACTION ({isolationLevel})");
                    try
                    {
                        double currentSalary = 0;
                        using (SqlCommand cmd = new SqlCommand("SELECT salar FROM Angajati WHERE cnp = @cnp", conn, tx))
                        {
                            cmd.Parameters.AddWithValue("@cnp", cnpTest1);
                            currentSalary = Convert.ToDouble(cmd.ExecuteScalar());
                            LogMessage($"Tranzactia A: A citit salariul {currentSalary}");
                        }

                        double newSalary = currentSalary + 1000;
                        LogMessage($"Tranzactia A: A calculat noul salariu (+1000): {newSalary}");

                        Task.Delay(3000).Wait();

                        using (SqlCommand cmd = new SqlCommand("UPDATE Angajati SET salar = @newSalary WHERE cnp = @cnp", conn, tx))
                        {
                            cmd.Parameters.AddWithValue("@cnp", cnpTest1);
                            cmd.Parameters.AddWithValue("@newSalary", newSalary);
                            cmd.ExecuteNonQuery();
                            LogMessage($"Tranzactia A: A actualizat salariul la {newSalary}");
                        }

                        tx.Commit();
                        LogMessage("Tranzactia A: COMMIT");
                    }
                    catch (Exception ex)
                    {
                        tx.Rollback();
                        LogMessage("Eroare Tx A: " + ex.Message);
                    }
                }
            }
        }

        private void RunLostUpdateProblemB(System.Data.IsolationLevel isolationLevel)
        {
            Task.Delay(1000).Wait();

            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();
                using (SqlTransaction tx = conn.BeginTransaction(isolationLevel))
                {
                    LogMessage($"Tranzactia B: BEGIN TRANSACTION ({isolationLevel})");
                    try
                    {
                        double currentSalary = 0;
                        using (SqlCommand cmd = new SqlCommand("SELECT salar FROM Angajati WHERE cnp = @cnp", conn, tx))
                        {
                            cmd.Parameters.AddWithValue("@cnp", cnpTest1);
                            currentSalary = Convert.ToDouble(cmd.ExecuteScalar());
                            LogMessage($"Tranzactia B: A citit salariul {currentSalary}");
                        }

                        double newSalary = currentSalary + 500;
                        LogMessage($"Tranzactia B: A calculat noul salariu (+500): {newSalary}");

                        using (SqlCommand cmd = new SqlCommand("UPDATE Angajati SET salar = @newSalary WHERE cnp = @cnp", conn, tx))
                        {
                            cmd.Parameters.AddWithValue("@cnp", cnpTest1);
                            cmd.Parameters.AddWithValue("@newSalary", newSalary);
                            cmd.ExecuteNonQuery();
                            LogMessage($"Tranzactia B: A actualizat salariul la {newSalary}");
                        }

                        tx.Commit();
                        LogMessage("Tranzactia B: COMMIT");
                    }
                    catch (Exception ex)
                    {
                        tx.Rollback();
                        LogMessage("Eroare Tx B: " + ex.Message);
                    }
                }
            }
        }

        // Metode pentru soluție 
        private void RunLostUpdateSolvedA()
        {
            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();
                using (SqlTransaction tx = conn.BeginTransaction(System.Data.IsolationLevel.ReadCommitted))
                {
                    LogMessage("Tranzactia A: BEGIN TRANSACTION (ReadCommitted)");
                    try
                    {
                        double currentSalary = 0;
                        using (SqlCommand cmd = new SqlCommand("SELECT salar FROM Angajati WHERE cnp = @cnp", conn, tx))
                        {
                            cmd.Parameters.AddWithValue("@cnp", cnpTest1);
                            currentSalary = Convert.ToDouble(cmd.ExecuteScalar());
                            LogMessage($"Tranzactia A: A citit salariul {currentSalary}");
                        }

                        double newSalary = currentSalary + 1000;
                        LogMessage($"Tranzactia A: A calculat noul salariu (+1000): {newSalary}");

                        Task.Delay(3000).Wait();

                        using (SqlCommand cmd = new SqlCommand(
                            "UPDATE Angajati SET salar = @newSalary WHERE cnp = @cnp AND salar = @oldSalary",
                            conn, tx))
                        {
                            cmd.Parameters.AddWithValue("@cnp", cnpTest1);
                            cmd.Parameters.AddWithValue("@newSalary", newSalary);
                            cmd.Parameters.AddWithValue("@oldSalary", currentSalary);

                            int rowsAffected = cmd.ExecuteNonQuery();
                            if (rowsAffected == 0)
                            {
                                LogMessage("Tranzactia A: Actualizare esuata (date modificate de alt tranzactie). Se face rollback.");
                                tx.Rollback();
                                return;
                            }
                            LogMessage($"Tranzactia A: A actualizat salariul la {newSalary}");
                        }

                        tx.Commit();
                        LogMessage("Tranzactia A: COMMIT");
                    }
                    catch (Exception ex)
                    {
                        tx.Rollback();
                        LogMessage("Eroare Tx A: " + ex.Message);
                    }
                }
            }
        }

        private void RunLostUpdateSolvedB()
        {
            Task.Delay(1000).Wait();

            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();
                using (SqlTransaction tx = conn.BeginTransaction(System.Data.IsolationLevel.ReadCommitted))
                {
                    LogMessage("Tranzactia B: BEGIN TRANSACTION (ReadCommitted) ");
                    try
                    {
                        double currentSalary = 0;
                        using (SqlCommand cmd = new SqlCommand("SELECT salar FROM Angajati WHERE cnp = @cnp", conn, tx))
                        {
                            cmd.Parameters.AddWithValue("@cnp", cnpTest1);
                            currentSalary = Convert.ToDouble(cmd.ExecuteScalar());
                            LogMessage($"Tranzactia B: A citit salariul {currentSalary}");
                        }

                        double newSalary = currentSalary + 500;
                        LogMessage($"Tranzactia B: A calculat noul salariu (+500): {newSalary}");

                        using (SqlCommand cmd = new SqlCommand(
                            "UPDATE Angajati SET salar = @newSalary WHERE cnp = @cnp AND salar = @oldSalary",
                            conn, tx))
                        {
                            cmd.Parameters.AddWithValue("@cnp", cnpTest1);
                            cmd.Parameters.AddWithValue("@newSalary", newSalary);
                            cmd.Parameters.AddWithValue("@oldSalary", currentSalary);

                            int rowsAffected = cmd.ExecuteNonQuery();
                            if (rowsAffected == 0)
                            {
                                LogMessage("Tranzactia B: Actualizare esuata (date modificate de alt tranzactie). Se face rollback.");
                                tx.Rollback();
                                return;
                            }
                            LogMessage($"Tranzactia B: A actualizat salariul la {newSalary}");
                        }

                        tx.Commit();
                        LogMessage("Tranzactia B: COMMIT");
                    }
                    catch (Exception ex)
                    {
                        tx.Rollback();
                        LogMessage("Eroare Tx B: " + ex.Message);
                    }
                }
            }
        }

        // ==========================================================
        // DEMONSTRATIE 5: DEADLOCK
        // ==========================================================

        private async void btnDeadlockProblem_Click(object sender, EventArgs e)
        {
            rtbLogs.Clear();
            LogMessage("=== START DEMO DEADLOCK (Apare Problema) ===");

            Task taskA = Task.Run(() => RunDeadlockTransactionA(false));
            Task taskB = Task.Run(() => RunDeadlockTransactionB(false));

            await Task.WhenAll(taskA, taskB);
            LogMessage("=== END DEMO ===" + Environment.NewLine);
        }

        private async void btnDeadlockSolved_Click(object sender, EventArgs e)
        {
            rtbLogs.Clear();
            LogMessage("=== START DEMO DEADLOCK (Prevenita prin ordonare) ===");

            // Parametrul 'true' forteaza Tx B sa acceseze datele in aceeasi ordine ca Tx A
            Task taskA = Task.Run(() => RunDeadlockTransactionA(true));
            Task taskB = Task.Run(() => RunDeadlockTransactionB(true));

            await Task.WhenAll(taskA, taskB);
            LogMessage("=== END DEMO ===" + Environment.NewLine);
        }

        private void RunDeadlockTransactionA(bool solved)
        {
            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();
                using (SqlTransaction tx = conn.BeginTransaction())
                {
                    LogMessage("Tranzactia A: BEGIN TRANSACTION");
                    try
                    {
                        LogMessage("Tranzactia A: Pune lock pe Angajat 1...");
                        UpdateSalaryForDeadlock(conn, tx, cnpTest1, 6000);
                        LogMessage("Tranzactia A: Angajat 1 blocat si actualizat.");

                        Task.Delay(2000).Wait();

                        LogMessage("Tranzactia A: Incearca sa puna lock pe Angajat 2...");
                        UpdateSalaryForDeadlock(conn, tx, cnpTest2, 7000);
                        LogMessage("Tranzactia A: Angajat 2 blocat si actualizat.");

                        tx.Commit();
                        LogMessage("Tranzactia A: COMMIT");
                    }
                    catch (SqlException ex)
                    {
                        tx.Rollback();
                        if (ex.Number == 1205) LogMessage("!!! DEADLOCK DETECTAT in Tx A !!!");
                        else LogMessage("Eroare SQL in Tx A: " + ex.Message);
                    }
                }
            }
        }

        private void RunDeadlockTransactionB(bool solved)
        {
            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();
                using (SqlTransaction tx = conn.BeginTransaction())
                {
                    LogMessage("Tranzactia B: BEGIN TRANSACTION");
                    try
                    {
                        string firstTarget = solved ? cnpTest1 : cnpTest2;
                        string secondTarget = solved ? cnpTest2 : cnpTest1;

                        LogMessage($"Tranzactia B: Pune lock pe Angajat {(solved ? "1" : "2")}...");
                        UpdateSalaryForDeadlock(conn, tx, firstTarget, 6500);
                        LogMessage($"Tranzactia B: Angajat {(solved ? "1" : "2")} blocat si actualizat.");

                        Task.Delay(2000).Wait();

                        LogMessage($"Tranzactia B: Incearca sa puna lock pe Angajat {(solved ? "2" : "1")}...");
                        UpdateSalaryForDeadlock(conn, tx, secondTarget, 7500);
                        LogMessage($"Tranzactia B: Angajat {(solved ? "2" : "1")} blocat si actualizat.");

                        tx.Commit();
                        LogMessage("Tranzactia B: COMMIT");
                    }
                    catch (SqlException ex)
                    {
                        tx.Rollback();
                        if (ex.Number == 1205) LogMessage("!!! DEADLOCK DETECTAT in Tx B !!! Baza de date a oprit aceasta tranzactie.");
                        else LogMessage("Eroare SQL in Tx B: " + ex.Message);
                    }
                }
            }
        }

        private void UpdateSalaryForDeadlock(SqlConnection conn, SqlTransaction tx, string cnp, double salary)
        {
            using (SqlCommand cmd = new SqlCommand("UPDATE Angajati SET salar = @sal WHERE cnp = @cnp", conn, tx))
            {
                cmd.Parameters.AddWithValue("@sal", salary);
                cmd.Parameters.AddWithValue("@cnp", cnp);
                cmd.ExecuteNonQuery();
            }
        }


        // ==========================================================
        // DEMONSTRATIE 6: TEST PERFORMANTA BATCH (3 METODE x 3 RULARI)
        // ==========================================================

        private void CleanUpBatchData()
        {
            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();
                using (SqlCommand cmd = new SqlCommand("DELETE FROM Angajati WHERE functie = 'TestBatch'", conn))
                {
                    cmd.ExecuteNonQuery();
                }
            }
        }

        private async void btnTestBatch_Click(object sender, EventArgs e)
        {
            rtbLogs.Clear();
            LogMessage("=== START TEST PERFORMANTA BATCH (5000 inserturi, 3 rulari) ===");
            LogMessage("Va dura cateva secunde... Te rog asteapta.\n");

            // Rulam operatiunile pe un task separat pentru a nu bloca interfata UI
            await Task.Run(() =>
            {
                long totalTimeAutoCommit = 0;
                long totalTimeBatched = 0;
                long totalTimeSingleTx = 0;
                int nrRulari = 3;

                for (int iteratie = 1; iteratie <= nrRulari; iteratie++)
                {
                    LogMessage($"--- Iteratia {iteratie} din {nrRulari} ---");

                    // 1. Auto-commit
                    CleanUpBatchData();
                    long time1 = RunBatchAutoCommit();
                    totalTimeAutoCommit += time1;
                    LogMessage($"Abordarea 1 (Auto-commit): {time1} ms");

                    // 2. Commit la 100 inregistrari
                    CleanUpBatchData();
                    long time2 = RunBatchChunked();
                    totalTimeBatched += time2;
                    LogMessage($"Abordarea 2 (Commit in loturi): {time2} ms");

                    // 3. O singura tranzactie (Commit final)
                    CleanUpBatchData();
                    long time3 = RunBatchSingleTx();
                    totalTimeSingleTx += time3;
                    LogMessage($"Abordarea 3 (Tranzactie unica): {time3} ms\n");
                }

                CleanUpBatchData();

                LogMessage("=== REZULTATE FINALE (MEDII) ===");
                LogMessage($"Media Auto-commit:\t\t{totalTimeAutoCommit / nrRulari} ms");
                LogMessage($"Media Commit in loturi:\t{totalTimeBatched / nrRulari} ms");
                LogMessage($"Media Tranzactie unica:\t{totalTimeSingleTx / nrRulari} ms");
                LogMessage("=== END TEST ===");
            });
        }

        private long RunBatchAutoCommit()
        {
            Stopwatch sw = Stopwatch.StartNew();
            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();
                string sql = "INSERT INTO Angajati (cnp, caen, nume, prenume, functie, salar, bonusuri) VALUES (@cnp, '5229', 'BatchName', 'BatchPrenume', 'TestBatch', 1000, 0)";

                for (int i = 0; i < 5000; i++)
                {
                    using (SqlCommand cmd = new SqlCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("@cnp", "B" + i.ToString().PadLeft(12, '0'));
                        cmd.ExecuteNonQuery(); // Auto-commit implicit la fiecare rulare
                    }
                }
            }
            sw.Stop();
            return sw.ElapsedMilliseconds;
        }

        private long RunBatchChunked()
        {
            Stopwatch sw = Stopwatch.StartNew();
            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();
                SqlTransaction tx = conn.BeginTransaction();
                string sql = "INSERT INTO Angajati (cnp, caen, nume, prenume, functie, salar, bonusuri) VALUES (@cnp, '5229', 'BatchName', 'BatchPrenume', 'TestBatch', 1000, 0)";

                for (int i = 0; i < 5000; i++)
                {
                    using (SqlCommand cmd = new SqlCommand(sql, conn, tx))
                    {
                        cmd.Parameters.AddWithValue("@cnp", "B" + i.ToString().PadLeft(12, '0'));
                        cmd.ExecuteNonQuery();
                    }

                    if ((i + 1) % 100 == 0)
                    {
                        tx.Commit();
                        if (i < 4999) tx = conn.BeginTransaction();
                    }
                }
            }
            sw.Stop();
            return sw.ElapsedMilliseconds;
        }

        private long RunBatchSingleTx()
        {
            Stopwatch sw = Stopwatch.StartNew();
            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();
                using (SqlTransaction tx = conn.BeginTransaction())
                {
                    string sql = "INSERT INTO Angajati (cnp, caen, nume, prenume, functie, salar, bonusuri) VALUES (@cnp, '5229', 'BatchName', 'BatchPrenume', 'TestBatch', 1000, 0)";

                    for (int i = 0; i < 5000; i++)
                    {
                        using (SqlCommand cmd = new SqlCommand(sql, conn, tx))
                        {
                            cmd.Parameters.AddWithValue("@cnp", "B" + i.ToString().PadLeft(12, '0'));
                            cmd.ExecuteNonQuery();
                        }
                    }
                    tx.Commit();
                }
            }
            sw.Stop();
            return sw.ElapsedMilliseconds;
        }


        // --- Metode Utilitare ---
        private void ResetSalaryTo(string cnp, double valoare)
        {
            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();
                using (SqlCommand cmd = new SqlCommand("UPDATE Angajati SET salar = @val WHERE cnp = @cnp", conn))
                {
                    cmd.Parameters.AddWithValue("@val", valoare);
                    cmd.Parameters.AddWithValue("@cnp", cnp);
                    cmd.ExecuteNonQuery();
                }
            }
        }

        private double GetCurrentSalary(string cnp)
        {
            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();
                using (SqlCommand cmd = new SqlCommand("SELECT salar FROM Angajati WHERE cnp = @cnp", conn))
                {
                    cmd.Parameters.AddWithValue("@cnp", cnp);
                    return Convert.ToDouble(cmd.ExecuteScalar());
                }
            }
        }
    }
}