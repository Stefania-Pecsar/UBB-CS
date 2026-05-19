using Microsoft.Data.SqlClient;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Caching.Memory;
using Microsoft.Extensions.Configuration;
using SGBD_lab3.Models;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Windows.Forms;

namespace SGBD_lab3
{
    public partial class Form1 : Form
    {
        private static IMemoryCache _cache = new MemoryCache(new MemoryCacheOptions());
        private int paginaCurenta = 0;
        private int pageSize = 10;
        private int cacheHits = 0;
        private int cacheMisses = 0;

        public Form1()
        {
            InitializeComponent();
            this.Load += Form1_Load;

            dgvParinte.SelectionChanged += DgvParinte_SelectionChanged;
            dgvCopil.SelectionChanged += DgvCopil_SelectionChanged;

            btnAdauga.Click += BtnAdauga_Click;
            btnModifica.Click += BtnModifica_Click;
            btnSterge.Click += BtnSterge_Click;
            btnTestA.Click += BtnTestA_Click;
            btnTestB.Click += BtnTestB_Click;
            btnTestB_Fixed.Click += BtnTestB_Fixed_Click;
            btnLazyEager.Click += BtnLazyVsEager_Click;

            btnN1.Click += BtnProblemaN1_Click;
            btnIndex.Click += BtnComparaIndex_Click;
            btnPaginare.Click += BtnPaginare_Click;
            btnCache.Click += BtnCaching_Click;
            btnBulk.Click += BtnBulkUpdate_Click;
            btnPreparedStatements.Click += BtnPreparedStatements_Click;

            btnNext.Click += BtnNext_Click;
            btnPrev.Click += BtnPrev_Click;
            cmbPageSize.SelectedIndexChanged += CmbPageSize_SelectedIndexChanged;
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            cmbPageSize.SelectedItem = "10";
            IncarcaFirme();
        }

        private void IncarcaFirme()
        {
            using (var context = new TransportContext())
            {
                dgvParinte.DataSource = context.FirmeTransport.ToList();
                if (dgvParinte.Columns["Angajati"] != null)
                {
                    dgvParinte.Columns["Angajati"].Visible = false;
                }
            }
        }

        private void DgvParinte_SelectionChanged(object sender, EventArgs e)
        {
            if (dgvParinte.CurrentRow != null)
            {
                paginaCurenta = 0;
                UpdatePaginare();
            }
        }

        private void DgvCopil_SelectionChanged(object sender, EventArgs e)
        {
            if (dgvCopil.CurrentRow != null)
            {
                txtCnp.Text = dgvCopil.CurrentRow.Cells["Cnp"].Value?.ToString();
                txtNume.Text = dgvCopil.CurrentRow.Cells["Nume"].Value?.ToString();
                txtPrenume.Text = dgvCopil.CurrentRow.Cells["Prenume"].Value?.ToString();
                txtFunctie.Text = dgvCopil.CurrentRow.Cells["Functie"].Value?.ToString();
                txtSalar.Text = dgvCopil.CurrentRow.Cells["Salar"].Value?.ToString();
                txtTelefon.Text = dgvCopil.CurrentRow.Cells["TelefonAngajat"].Value?.ToString();
            }
        }

        private void ClearTextBoxes()
        {
            txtCnp.Clear();
            txtNume.Clear();
            txtPrenume.Clear();
            txtFunctie.Clear();
            txtSalar.Clear();
            txtTelefon.Clear();
        }

        private void BtnGenereazaDate_Click(object sender, EventArgs e)
        {
            using (var context = new TransportContext())
            {
                var caenList = context.FirmeTransport.Select(f => f.Caen).ToList();
                if (!caenList.Any())
                {
                    MessageBox.Show("Adaugă cel puțin o firmă de transport mai întâi!");
                    return;
                }

                var rnd = new Random();
                var angajatiNoi = new List<Angajat>();

                for (int i = 0; i < 10000; i++)
                {
                    angajatiNoi.Add(new Angajat
                    {
                        Cnp = "1" + rnd.Next(100000, 999999).ToString() + rnd.Next(10000, 99999).ToString(),
                        Caen = caenList[rnd.Next(caenList.Count)],
                        Nume = "TestNume_" + i,
                        Prenume = "TestPrenume",
                        Functie = "Sofer",
                        Salar = rnd.Next(3000, 15000),
                        TelefonAngajat = "07" + rnd.Next(10000000, 99999999).ToString(),
                        Bonusuri = rnd.Next(100, 1000)
                    });
                }

                context.Angajati.AddRange(angajatiNoi);
                context.SaveChanges();
                MessageBox.Show("10.000 de angajați au fost generați cu succes!");
            }
        }

        private string ultimulCnpKeyset = "";
        private Stack<string> istoricKeyset = new Stack<string>();

        private void UpdatePaginare()
        {
            if (dgvParinte.CurrentRow == null) return;
            string caenSelectat = dgvParinte.CurrentRow.Cells["Caen"].Value.ToString();

            using (var context = new TransportContext())
            {
                IQueryable<Angajat> bazaQuery;

                if (chkVeziSterse.Checked)
                {
                    bazaQuery = context.Angajati
                                       .IgnoreQueryFilters()
                                       .Where(a => a.Caen == caenSelectat && a.IsDeleted == true)
                                       .OrderBy(a => a.Cnp);
                }
                else
                {
                    bazaQuery = context.Angajati
                                       .Where(a => a.Caen == caenSelectat)
                                       .OrderBy(a => a.Cnp);
                }

                lblTotal.Text = $"Total: {bazaQuery.Count()}";

                if (rbOffset.Checked)
                {
                    dgvCopil.DataSource = bazaQuery.Skip(paginaCurenta * pageSize).Take(pageSize).ToList();
                    lblPagina.Text = $"Pagina: {paginaCurenta + 1}";
                }
                else
                {
                    var queryKeyset = string.IsNullOrEmpty(ultimulCnpKeyset)
                        ? bazaQuery
                        : bazaQuery.Where(a => string.Compare(a.Cnp, ultimulCnpKeyset) > 0);

                    var rezultate = queryKeyset.Take(pageSize).ToList();
                    dgvCopil.DataSource = rezultate;

                    if (rezultate.Any()) ultimulCnpKeyset = rezultate.Last().Cnp;
                    lblPagina.Text = $"Keyset (Adancime: {istoricKeyset.Count})";
                }

                string[] coloaneDeAscuns = { "RowVersion", "IsDeleted", "DeletedAt", "DeletedBy", "FirmaTransport" };
                foreach (var col in coloaneDeAscuns)
                {
                    if (dgvCopil.Columns[col] != null) dgvCopil.Columns[col].Visible = false;
                }

                if (dgvCopil.Columns["TelefonAngajat"] != null)
                    dgvCopil.Columns["TelefonAngajat"].Visible = true;
            }
        }

        private void chkVeziSterse_CheckedChanged(object sender, EventArgs e)
        {
            paginaCurenta = 0;
            UpdatePaginare();
        }

        private void btnRestaureaza_Click(object sender, EventArgs e)
        {
            if (dgvCopil.CurrentRow == null) return;
            string cnpSelectat = txtCnp.Text;

            try
            {
                using (var context = new TransportContext())
                {
                    var angajat = context.Angajati.IgnoreQueryFilters().FirstOrDefault(a => a.Cnp == cnpSelectat);

                    if (angajat != null && angajat.IsDeleted)
                    {
                        angajat.IsDeleted = false;
                        angajat.DeletedAt = null;
                        angajat.DeletedBy = "";

                        context.SaveChanges();
                        MessageBox.Show("Angajatul a fost restaurat cu succes!");

                        chkVeziSterse.Checked = false;
                        UpdatePaginare();
                    }
                    else
                    {
                        MessageBox.Show("Selectează un angajat șters pentru a-l restaura.");
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Eroare la restaurare: " + ex.Message);
            }
        }

        private void BtnCauta_Click(object sender, EventArgs e)
        {
            string cnp = txtCautareCnp.Text.Trim();
            if (string.IsNullOrEmpty(cnp))
            {
                lblStareAngajat.Text = "Introdu un CNP.";
                return;
            }

            using (var context = new TransportContext())
            {
                var angajat = context.Angajati
                    .IgnoreQueryFilters()
                    .FirstOrDefault(a => a.Cnp == cnp);

                if (angajat == null)
                {
                    lblStareAngajat.Text = "❌ CNP negăsit.";
                }
                else if (angajat.IsDeleted)
                {
                    lblStareAngajat.Text = $"⚠️ Angajat ȘTERS (de {angajat.DeletedBy} la {angajat.DeletedAt:yyyy-MM-dd HH:mm})";
                }
                else
                {
                    lblStareAngajat.Text = $"✅ Angajat ACTIV: {angajat.Nume} {angajat.Prenume}, funcția {angajat.Functie}";
                }
            }
        }

        private void BtnNext_Click(object sender, EventArgs e)
        {
            if (rbOffset.Checked) paginaCurenta++;
            else istoricKeyset.Push(ultimulCnpKeyset);
            UpdatePaginare();
        }

        private void BtnPrev_Click(object sender, EventArgs e)
        {
            if (rbOffset.Checked) { if (paginaCurenta > 0) paginaCurenta--; }
            else if (istoricKeyset.Count > 0)
            {
                istoricKeyset.Pop();
                ultimulCnpKeyset = istoricKeyset.Count > 0 ? istoricKeyset.Peek() : "";
            }
            UpdatePaginare();
        }

        private void CmbPageSize_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (int.TryParse(cmbPageSize.SelectedItem?.ToString(), out int newSize))
            {
                pageSize = newSize;
                paginaCurenta = 0;
                UpdatePaginare();
            }
        }

        private void BtnAdauga_Click(object sender, EventArgs e)
        {
            if (dgvParinte.CurrentRow == null) return;
            string caenSelectat = dgvParinte.CurrentRow.Cells["Caen"].Value.ToString();

            try
            {
                using (var context = new TransportContext())
                using (var transaction = context.Database.BeginTransaction())
                {
                    var angajatNou = new Angajat
                    {
                        Cnp = txtCnp.Text,
                        Caen = caenSelectat,
                        Nume = txtNume.Text,
                        Prenume = txtPrenume.Text,
                        Functie = txtFunctie.Text,
                        Salar = decimal.Parse(txtSalar.Text),
                        Bonusuri = 1000,
                        TelefonAngajat = txtTelefon.Text,
                        DeletedBy = "",
                        IsDeleted = false
                    };

                    context.Angajati.Add(angajatNou);
                    context.SaveChanges();
                    transaction.Commit();

                    UpdatePaginare();
                    ClearTextBoxes();
                    MessageBox.Show("Angajat adăugat cu succes!");
                }
            }
            catch (Exception ex)
            {
                string mesajEroare = ex.Message;
                if (ex.InnerException != null)
                {
                    mesajEroare += "\n\nDetalii (Inner Exception):\n" + ex.InnerException.Message;
                }
                MessageBox.Show("Eroare la adăugare:\n" + mesajEroare, "Eroare Bază de Date", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void BtnModifica_Click(object sender, EventArgs e)
        {
            if (dgvCopil.CurrentRow == null) return;
            string cnp = txtCnp.Text;

            try
            {
                using (var context = new TransportContext())
                using (var transaction = context.Database.BeginTransaction())
                {
                    var angajat = context.Angajati.Find(cnp);
                    if (angajat != null)
                    {
                        angajat.Nume = txtNume.Text;
                        angajat.Prenume = txtPrenume.Text;
                        angajat.Functie = txtFunctie.Text;
                        angajat.Salar = decimal.Parse(txtSalar.Text);
                        angajat.TelefonAngajat = txtTelefon.Text;

                        context.SaveChanges();
                        transaction.Commit();
                        UpdatePaginare();
                        _cache.Remove($"firma_{angajat.Caen}");
                        MessageBox.Show("Modificare salvată!");
                    }
                }
            }
            catch (DbUpdateConcurrencyException)
            {
                MessageBox.Show("Conflict de versiune! Cineva a modificat datele înaintea ta. Datele se vor reîmprospăta.", "Eroare Concurență", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                UpdatePaginare();
            }
            catch (Exception ex)
            {
                MessageBox.Show("Eroare la modificare: " + ex.Message);
            }
        }

        private void BtnSterge_Click(object sender, EventArgs e)
        {
            if (dgvCopil.CurrentRow == null) return;
            string cnpSelectat = txtCnp.Text;

            var confirmResult = MessageBox.Show("Ești sigur că vrei să ștergi acest angajat?", "Confirmare", MessageBoxButtons.YesNo);
            if (confirmResult != DialogResult.Yes) return;

            try
            {
                using (var context = new TransportContext())
                {
                    var angajat = context.Angajati.Find(cnpSelectat);
                    if (angajat != null)
                    {
                        angajat.IsDeleted = true;
                        angajat.DeletedAt = DateTime.Now;
                        angajat.DeletedBy = Environment.UserName;

                        context.SaveChanges();
                        UpdatePaginare();
                        ClearTextBoxes();
                        MessageBox.Show("Angajatul a fost șters logic (soft delete)!");
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Eroare la ștergere: " + ex.Message);
            }
        }

        private void BtnTestA_Click(object sender, EventArgs e)
        {
            var config = new ConfigurationBuilder().SetBasePath(Directory.GetCurrentDirectory()).AddJsonFile("appsettings.json").Build();
            string connPooling = config.GetConnectionString("DefaultConnection");
            string connNoPooling = config.GetConnectionString("NoPoolingConnection");

            Stopwatch sw = new Stopwatch();

            sw.Start();
            for (int i = 0; i < 100; i++)
            {
                using (SqlConnection conn = new SqlConnection(connNoPooling))
                {
                    conn.Open();
                }
            }
            sw.Stop();
            long timeNoPooling = sw.ElapsedMilliseconds;

            sw.Reset();
            sw.Start();
            for (int i = 0; i < 100; i++)
            {
                using (SqlConnection conn = new SqlConnection(connPooling))
                {
                    conn.Open();
                }
            }
            sw.Stop();
            long timeWithPooling = sw.ElapsedMilliseconds;

            MessageBox.Show($"Timp FĂRĂ pooling (100 conexiuni): {timeNoPooling} ms\nTimp CU pooling (100 conexiuni): {timeWithPooling} ms");
        }

        private void BtnTestB_Click(object sender, EventArgs e)
        {
            var config = new ConfigurationBuilder().SetBasePath(Directory.GetCurrentDirectory()).AddJsonFile("appsettings.json").Build();
            string connPooling = config.GetConnectionString("DefaultConnection");

            SqlConnection[] connections = new SqlConnection[15];
            try
            {
                for (int i = 0; i < 15; i++)
                {
                    connections[i] = new SqlConnection(connPooling);
                    connections[i].Open();
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Scurgere de conexiuni detectată:\n" + ex.Message);
            }
        }

        private void BtnTestLocking_Click(object sender, EventArgs e)
        {
            
            if (dgvCopil.CurrentRow == null)
            {
                MessageBox.Show("Selectează un angajat din tabelul copil.");
                return;
            }
            string cnpTest = dgvCopil.CurrentRow.Cells["Cnp"].Value.ToString();

            using (var contextA = new TransportContext())
            using (var contextB = new TransportContext())
            {
                var angajatA = contextA.Angajati.IgnoreQueryFilters().FirstOrDefault(a => a.Cnp == cnpTest);
                var angajatB = contextB.Angajati.IgnoreQueryFilters().FirstOrDefault(a => a.Cnp == cnpTest);

                if (angajatA == null || angajatB == null)
                {
                    MessageBox.Show($"Angajatul cu CNP {cnpTest} nu există.");
                    return;
                }

                // Salvează versiunea inițială (doar pentru informare)
                byte[] versiuneInitiala = angajatA.RowVersion;

                // Pas 1: A modifică și salvează
                angajatA.Salar += 100;
                contextA.SaveChanges();

                // Pas 2: B încearcă să salveze cu datele vechi (încărcate inițial)
                angajatB.Salar += 50;
                try
                {
                    contextB.SaveChanges();
                    MessageBox.Show("Nu s-a produs conflict (ceva neașteptat).");
                }
                catch (DbUpdateConcurrencyException ex)
                {
                    var entry = ex.Entries.Single();
                    var databaseValues = entry.GetDatabaseValues();

                    string logMessage = $"{DateTime.Now:yyyy-MM-dd HH:mm:ss} - Conflict concurență pentru angajatul {angajatB.Cnp} - {angajatB.Nume} {angajatB.Prenume}\n" +
                        $"Salariu utilizator: {angajatB.Salar}, Salariu DB: {databaseValues["Salar"]}\n" +
                        $"Excepție: {ex.Message}\n{new string('-', 50)}\n";
                    File.AppendAllText("concurrency_log.txt", logMessage);

                    DialogResult rezultat = MessageBox.Show(
                        $"Conflict de concurență pentru {angajatB.Nume} {angajatB.Prenume}\n\n" +
                        $"Salariul tău: {angajatB.Salar}\n" +
                        $"Salariu în DB: {databaseValues["Salar"]}\n\n" +
                        "Ce faci?\nYes = Reîncarcă datele\nNo = Suprascrie\nCancel = Anulează",
                        "Locking optimist",
                        MessageBoxButtons.YesNoCancel);

                    if (rezultat == DialogResult.Yes)
                    {
                        entry.Reload();
                        MessageBox.Show("Date reîncărcate.");
                    }
                    else if (rezultat == DialogResult.No)
                    {
                        entry.OriginalValues.SetValues(databaseValues);
                        contextB.SaveChanges();
                        MessageBox.Show("Suprascriere forțată realizată.");
                    }
                    else
                    {
                        MessageBox.Show("Operație anulată.");
                    }
                }
                UpdatePaginare();
            }
        }

        private void BtnStergePermanent_Click(object sender, EventArgs e)
        {
            if (dgvCopil.CurrentRow == null) return;
            string cnp = dgvCopil.CurrentRow.Cells["Cnp"].Value.ToString();

            // Opțional: confirmare
            if (MessageBox.Show($"Ștergi DEFINITIV angajatul cu CNP {cnp}?\nAcțiunea este ireversibilă!",
                "Confirmare hard delete", MessageBoxButtons.YesNo, MessageBoxIcon.Warning) != DialogResult.Yes)
                return;

            try
            {
                using (var context = new TransportContext())
                {
                    // Trebuie să ignorăm filtrul global pentru a găsi și înregistrările șterse logic
                    var angajat = context.Angajati.IgnoreQueryFilters().FirstOrDefault(a => a.Cnp == cnp);
                    if (angajat != null)
                    {
                        context.Angajati.Remove(angajat);
                        context.SaveChanges();
                        MessageBox.Show("Angajat șters definitiv.");
                        UpdatePaginare();
                        ClearTextBoxes();
                    }
                    else
                    {
                        MessageBox.Show("Angajatul nu a fost găsit.");
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Eroare la ștergerea permanentă: " + ex.Message);
            }
        }

        private void btnArataProiecte_Click(object sender, EventArgs e)
        {
            using (var context = new TransportContext())
            {
                var proiecte = context.Proiect.ToList();
                string mesaj = string.Join(Environment.NewLine, proiecte.Select(p => $"{p.Nume} - {p.Descriere} (Firma: {p.CaenFirma})"));
                MessageBox.Show(mesaj, "Lista proiecte");
            }
        }

        private void BtnTestB_Fixed_Click(object sender, EventArgs e)
        {
            var config = new ConfigurationBuilder().SetBasePath(Directory.GetCurrentDirectory()).AddJsonFile("appsettings.json").Build();
            string connPooling = config.GetConnectionString("DefaultConnection");

            try
            {
                for (int i = 0; i < 15; i++)
                {
                    using (SqlConnection conn = new SqlConnection(connPooling))
                    {
                        conn.Open();
                    }
                }
                MessageBox.Show("Success! 15 conexiuni create si inchise corect. Pool-ul NU s-a epuizat.");
            }
            catch (Exception ex)
            {
                MessageBox.Show("Eroare: " + ex.Message);
            }
        }

        private void BtnLazyVsEager_Click(object sender, EventArgs e)
        {
            BtnProblemaN1_Click(sender, e);
        }

        private string CaptureSqlLogs(Action action)
        {
            var original = Console.Out;
            using (var sw = new StringWriter())
            {
                Console.SetOut(sw);
                action();
                Console.SetOut(original);
                return sw.ToString();
            }
        }

        private void BtnProblemaN1_Click(object sender, EventArgs e)
        {
            long timpLazy = 0, timpEager = 0;

            string lazyLogs = CaptureSqlLogs(() => {
                using (var context = new TransportContext())
                {
                    var sw = Stopwatch.StartNew();
                    var firme = context.FirmeTransport.ToList();
                    int totalAngajati = 0;
                    foreach (var f in firme) { totalAngajati += f.Angajati.Count; }
                    sw.Stop();
                    timpLazy = sw.ElapsedMilliseconds;
                }
            });

            string eagerLogs = CaptureSqlLogs(() => {
                using (var context = new TransportContext())
                {
                    var sw = Stopwatch.StartNew();
                    var firme = context.FirmeTransport.Include(f => f.Angajati).ToList();
                    int totalAngajati = 0;
                    foreach (var f in firme) { totalAngajati += f.Angajati.Count; }
                    sw.Stop();
                    timpEager = sw.ElapsedMilliseconds;
                }
            });

            int qLazy = lazyLogs.Split(new[] { "SELECT" }, StringSplitOptions.None).Length - 1;
            int qEager = eagerLogs.Split(new[] { "SELECT" }, StringSplitOptions.None).Length - 1;

            MessageBox.Show($"=== COMPARAȚIE N+1 ===\n\nScenariu LAZY:\n- Timp: {timpLazy} ms\n- Interogări SQL: {qLazy}\n\nScenariu EAGER:\n- Timp: {timpEager} ms\n- Interogări SQL: {qEager}\n", "Lab 4 - Sarcina 1");
        }

        private void BtnComparaIndex_Click(object sender, EventArgs e)
        {
            using (var context = new TransportContext())
            {
                ExecutaSqlIgnorandErori(context, "DROP INDEX idx_angajati_nume ON Angajati");
                ExecutaSqlIgnorandErori(context, "DROP INDEX idx_angajati_caen ON Angajati");
                ExecutaSqlIgnorandErori(context, "DROP INDEX idx_angajati_salar ON Angajati");
                ExecutaSqlIgnorandErori(context, "DROP INDEX idx_angajati_caen_salar ON Angajati");

                var timpiFara = RuleazaBenchmark(context);

                context.Database.ExecuteSqlRaw("CREATE INDEX idx_angajati_nume ON Angajati (Nume)");
                context.Database.ExecuteSqlRaw("CREATE INDEX idx_angajati_caen ON Angajati (Caen)");
                context.Database.ExecuteSqlRaw("CREATE INDEX idx_angajati_salar ON Angajati (Salar)");
                context.Database.ExecuteSqlRaw("CREATE INDEX idx_angajati_caen_salar ON Angajati (Caen, Salar)");

                var timpiCu = RuleazaBenchmark(context);

                MessageBox.Show(
                    $"=== BENCHMARK INDEXARE (100 runs) ===\n\n" +
                    $"1. Nume: Fără = {timpiFara[0]}ms | Cu = {timpiCu[0]}ms\n" +
                    $"2. Caen: Fără = {timpiFara[1]}ms | Cu = {timpiCu[1]}ms\n" +
                    $"3. Interval Salar: Fără = {timpiFara[2]}ms | Cu = {timpiCu[2]}ms\n" +
                    $"4. Multi-coloană: Fără = {timpiFara[3]}ms | Cu = {timpiCu[3]}ms"
                );
            }
        }

        private double[] RuleazaBenchmark(TransportContext context)
        {
            var sw = new Stopwatch();
            double[] rez = new double[4];
            int runs = 100;

            sw.Restart(); for (int i = 0; i < runs; i++) context.Angajati.Where(a => a.Nume == "TestNume_500").ToList();
            rez[0] = sw.ElapsedMilliseconds / (double)runs;

            sw.Restart(); for (int i = 0; i < runs; i++) context.Angajati.Where(a => a.Caen == "1010").ToList();
            rez[1] = sw.ElapsedMilliseconds / (double)runs;

            sw.Restart(); for (int i = 0; i < runs; i++) context.Angajati.Where(a => a.Salar > 5000 && a.Salar < 8000).ToList();
            rez[2] = sw.ElapsedMilliseconds / (double)runs;

            sw.Restart(); for (int i = 0; i < runs; i++) context.Angajati.Where(a => a.Caen == "1010" && a.Salar > 6000).ToList();
            rez[3] = sw.ElapsedMilliseconds / (double)runs;

            return rez;
        }

        private void ExecutaSqlIgnorandErori(TransportContext ctx, string sql)
        {
            try { ctx.Database.ExecuteSqlRaw(sql); } catch { }
        }

        private void BtnPaginare_Click(object sender, EventArgs e)
        {
            using (var context = new TransportContext())
            {
                var sw = Stopwatch.StartNew();
                var p1 = context.Angajati.OrderBy(a => a.Cnp).Skip(20).Take(10).ToList();
                sw.Stop();
                long t1 = sw.ElapsedMilliseconds;

                sw.Restart();
                var p2 = context.Angajati.OrderBy(a => a.Cnp).Where(a => string.Compare(a.Cnp, "100") > 0).Take(10).ToList();
                sw.Stop();
                long t2 = sw.ElapsedMilliseconds;

                MessageBox.Show($"Paginare OFFSET (Skip/Take): {t1} ms\nPaginare KEYSET/CURSOR: {t2} ms", "Lab 4 - Sarcina 3");
            }
        }

        private void BtnCaching_Click(object sender, EventArgs e)
        {
            if (dgvParinte.CurrentRow == null) return;
            string idFirma = dgvParinte.CurrentRow.Cells["Caen"].Value.ToString();
            string key = $"firma_{idFirma}";

            var sw = Stopwatch.StartNew();
            if (!_cache.TryGetValue(key, out FirmaTransport firma))
            {
                cacheMisses++;
                using (var context = new TransportContext())
                {
                    firma = context.FirmeTransport.AsNoTracking().FirstOrDefault(f => f.Caen == idFirma);
                }
                _cache.Set(key, firma, TimeSpan.FromMinutes(5));
                sw.Stop();
                AfiseazaStatisticiCache($"MISS - Incarcat din DB ({sw.ElapsedMilliseconds}ms)");
            }
            else
            {
                cacheHits++;
                sw.Stop();
                AfiseazaStatisticiCache($"HIT - Incarcat din RAM ({sw.ElapsedMilliseconds}ms)");
            }
        }

        private void AfiseazaStatisticiCache(string status)
        {
            double total = cacheHits + cacheMisses;
            double hitRate = total > 0 ? (cacheHits / total) * 100 : 0;
            MessageBox.Show($"{status}\n\nStatistici:\nHits: {cacheHits}\nMisses: {cacheMisses}\nHit Rate: {hitRate:F2}%", "Lab 4 - Sarcina 4");
        }

        private void BtnBulkUpdate_Click(object sender, EventArgs e)
        {
            long tIndividual = 0, tBulk = 0, tBatch = 0;
            int count = 1000;

            using (var context = new TransportContext())
            {
                var lista1 = context.Angajati.Take(count).ToList();
                var sw = Stopwatch.StartNew();
                foreach (var a in lista1)
                {
                    a.Salar *= 1.01m;
                    context.Update(a);
                    context.SaveChanges();
                }
                tIndividual = sw.ElapsedMilliseconds;

                sw.Restart();
                context.Database.ExecuteSqlRaw("UPDATE Angajati SET Salar = Salar * 1.01 WHERE IsDeleted = 0");
                tBulk = sw.ElapsedMilliseconds;

                sw.Restart();
                var lista2 = context.Angajati.Take(count).ToList();
                int batchSize = 50;

                for (int i = 0; i < lista2.Count; i++)
                {
                    var a = lista2[i];
                    a.Salar *= 1.01m;
                    context.Update(a);

                    if (i > 0 && i % batchSize == 0)
                    {
                        context.SaveChanges();
                        context.ChangeTracker.Clear();
                    }
                }
                context.SaveChanges();
                tBatch = sw.ElapsedMilliseconds;

                MessageBox.Show($"Individual: {tIndividual}ms\nBulk SQL (Protected): {tBulk}ms\nBatch EF (50 records): {tBatch}ms", "Lab 4 & 5 - Optimizare");
                UpdatePaginare();
            }
        }

        private void BtnExplain_Click(object sender, EventArgs e)
        {
            using (var context = new TransportContext())
            {
                var conn = context.Database.GetDbConnection();
                conn.Open();

                using (var cmd = conn.CreateCommand())
                {
                    cmd.CommandText = "SET STATISTICS PROFILE ON;";
                    cmd.ExecuteNonQuery();
                }

                string planOutput = "";

                using (var cmd = conn.CreateCommand())
                {
                    cmd.CommandText = "SELECT * FROM Angajati WHERE Caen = '1010' AND Salar > 6000";

                    using (var reader = cmd.ExecuteReader())
                    {
                        if (reader.NextResult())
                        {
                            while (reader.Read())
                            {
                                planOutput += reader["StmtText"].ToString() + "\n";
                            }
                        }
                    }
                }

                using (var cmd = conn.CreateCommand())
                {
                    cmd.CommandText = "SET STATISTICS PROFILE OFF;";
                    cmd.ExecuteNonQuery();
                }

                if (string.IsNullOrEmpty(planOutput))
                {
                    MessageBox.Show("Nu s-a putut captura planul.", "Eroare");
                }
                else
                {
                    MessageBox.Show($"Plan execuție (EXPLAIN ANALYZE equivalent):\n\n{planOutput}", "EXPLAIN ANALYZE - SQL Server");
                }
            }
        }

        private void BtnPreparedStatements_Click(object sender, EventArgs e)
        {
            var config = new ConfigurationBuilder().SetBasePath(Directory.GetCurrentDirectory()).AddJsonFile("appsettings.json").Build();
            string connStr = config.GetConnectionString("DefaultConnection");

            var sw = Stopwatch.StartNew();
            for (int i = 0; i < 500; i++)
            {
                using (var conn = new SqlConnection(connStr))
                {
                    conn.Open();
                    var cmd = new SqlCommand("SELECT COUNT(*) FROM Angajati WHERE Salar > @s", conn);
                    cmd.Parameters.AddWithValue("@s", 5000 + i);
                    cmd.ExecuteScalar();
                }
            }
            long tNoReuse = sw.ElapsedMilliseconds;

            sw.Restart();
            using (var conn = new SqlConnection(connStr))
            {
                conn.Open();
                var cmd = new SqlCommand("SELECT COUNT(*) FROM Angajati WHERE Salar > @s", conn);
                var param = cmd.Parameters.Add("@s", System.Data.SqlDbType.Float);
                cmd.Prepare();
                for (int i = 0; i < 500; i++)
                {
                    param.Value = 5000 + i;
                    cmd.ExecuteScalar();
                }
            }
            long tReuse = sw.ElapsedMilliseconds;

            MessageBox.Show($"Fără reutilizare: {tNoReuse}ms\nCu Prepared Statement: {tReuse}ms", "Lab 4 - Sarcina 6");
        }
    }
}