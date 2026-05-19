<<<<<<< Updated upstream
﻿using Microsoft.Data.SqlClient;
using System;
using System.Collections.Generic;
using System.Data;
using System.Windows.Forms;

namespace SGBD_lab1
{
    public partial class Form1 : Form
    {
        private DatabaseService dbService = new DatabaseService();
        private DataSet dataSet = new DataSet();
        private BindingSource bsParent = new BindingSource();
        private BindingSource bsChild = new BindingSource();

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            LoadData();
        }

        //incarcare date
        private void LoadData()
        {
            try
            {
                using (SqlConnection connection = new SqlConnection(dbService.ConnectionString))
                {
                    connection.Open();

                    SqlDataAdapter parentAdapter = new SqlDataAdapter("SELECT * FROM Firma_transport", connection);
                    SqlDataAdapter childAdapter = new SqlDataAdapter("SELECT * FROM Angajati", connection);

                    dataSet.Clear();
                    if (dataSet.Relations.Contains("FK_Firma_transport_Angajati"))
                        dataSet.Relations.Remove("FK_Firma_transport_Angajati");

                    parentAdapter.Fill(dataSet, "Firma_transport");
                    childAdapter.Fill(dataSet, "Angajati");

                    DataColumn pkColumn = dataSet.Tables["Firma_transport"].Columns["caen"];
                    DataColumn fkColumn = dataSet.Tables["Angajati"].Columns["caen"];

                    // stabilire relație 1-n  
                    DataRelation relation = new DataRelation("FK_Firma_transport_Angajati", pkColumn, fkColumn);
                    dataSet.Relations.Add(relation);

                    bsParent.DataSource = dataSet.Tables["Firma_transport"];
                    FIrma_DGW.DataSource = bsParent;

                    bsChild.DataSource = bsParent;
                    bsChild.DataMember = "FK_Firma_transport_Angajati";
                    Angajati_DGW.DataSource = bsChild;

                    // DataBinding pentru editare ușoară
                    ClearBindings();
                    tb_caen.DataBindings.Add("Text", bsChild, "caen", true);
                    tb_nume.DataBindings.Add("Text", bsChild, "nume", true);
                    tb_prenume.DataBindings.Add("Text", bsChild, "prenume", true);
                    tb_functie.DataBindings.Add("Text", bsChild, "functie", true);
                    tb_salar.DataBindings.Add("Text", bsChild, "salar", true);
                    tb_bonusuri.DataBindings.Add("Text", bsChild, "bonusuri", true);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Eroare la încărcare: " + ex.Message);
            }
        }

        private void ClearBindings()
        {
            tb_caen.DataBindings.Clear();
            tb_nume.DataBindings.Clear();
            tb_prenume.DataBindings.Clear();
            tb_functie.DataBindings.Clear();
            tb_salar.DataBindings.Clear();
            tb_bonusuri.DataBindings.Clear();
        }

        //buton refresh
        private void btn_refresh_Click(object sender, EventArgs e)
        {
            LoadData(); 
            MessageBox.Show("Date reîncărcate cu succes!");
        }

        //buton adaugare
        private void btn_Add_Click(object sender, EventArgs e)
        {
            //   selectam firma
            if (FIrma_DGW.CurrentRow != null && ValidateAdaugare())
            {
                try
                {
                    // preluam caen de la randul cuurent
                    string caen = FIrma_DGW.CurrentRow.Cells["caen"].Value.ToString();
                    string query = "INSERT INTO Angajati(cnp, caen, nume, prenume, functie, salar, bonusuri) VALUES (@cnp, @caen, @nume, @prenume, @functie, @salar, @bonusuri)";

                    var parameters = new List<SqlParameter>
            {
                new SqlParameter("@cnp", tb_cnpFT.Text),
                new SqlParameter("@caen", caen),
                new SqlParameter("@nume", tb_numeFT.Text),
                new SqlParameter("@prenume", tb_prenumeFT.Text),
                new SqlParameter("@functie", tb_functieFT.Text),
                new SqlParameter("@salar", decimal.Parse(tb_salarFT.Text)),
                new SqlParameter("@bonusuri", decimal.Parse(tb_bonusuriFT.Text))
            };
                    dbService.ExecuteNonQuery(query, parameters);

                    tb_cnpFT.Clear();
                    tb_numeFT.Clear();
                    tb_prenumeFT.Clear();
                    tb_functieFT.Clear();
                    tb_salarFT.Clear();
                    tb_bonusuriFT.Clear();
                    LoadData();
                    MessageBox.Show("Angajat adăugat cu succes!");
                }
                catch (Exception ex)
                {
                    MessageBox.Show("Eroare la adăugare: " + ex.Message);
                }
            }
            else
            {
                MessageBox.Show("Vă rugăm să selectați o firmă și să completați corect datele!");
            }
        }

        //buton actualizare
        private void btn_Update_Click(object sender, EventArgs e)
        {
            // vf. daca exista un rand selectat 
            if (Angajati_DGW.CurrentRow != null)
            {
                if (ValidateUpdate())
                {
                    try
                    {
                        string cnp = Angajati_DGW.CurrentRow.Cells["cnp"].Value.ToString();
                        string query = "UPDATE Angajati SET nume=@nume, prenume=@prenume, functie=@functie, salar=@salar, bonusuri=@bonusuri WHERE cnp=@cnp";

                        var parameters = new List<SqlParameter>
                {
                    new SqlParameter("@nume", tb_nume.Text),
                    new SqlParameter("@prenume", tb_prenume.Text),
                    new SqlParameter("@functie", tb_functie.Text),
                    new SqlParameter("@salar", decimal.Parse(tb_salar.Text)),
                    new SqlParameter("@bonusuri", decimal.Parse(tb_bonusuri.Text)),
                    new SqlParameter("@cnp", cnp)
                };

                        dbService.ExecuteNonQuery(query, parameters);
                        LoadData();
                        MessageBox.Show("Actualizare realizata cu succes!", "Succes", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show("Eroare la baza de date: " + ex.Message, "Eroare", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                }
            }
            else
            {
                MessageBox.Show("Vă rugăm să selectați angajatul pe care doriți să îl modificați din tabel!", "Atenție", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }

        private void btn_Delete_Click(object sender, EventArgs e)
        {
            if (Angajati_DGW.SelectedRows.Count == 1)
            {
                if (MessageBox.Show("Sigur ștergeți acest angajat?", "Confirmare", MessageBoxButtons.YesNo) == DialogResult.Yes)
                {
                    try
                    {
                        string cnp = Angajati_DGW.SelectedRows[0].Cells["cnp"].Value.ToString();
                        string query = "DELETE FROM Angajati WHERE cnp = @cnp";
                        var parameters = new List<SqlParameter> { new SqlParameter("@cnp", cnp) };
                        dbService.ExecuteNonQuery(query, parameters);
                        LoadData();
                        MessageBox.Show("Angajat șters!");
                    }
                    catch (SqlException ex)
                    {
                        MessageBox.Show("Eroare bază de date: " + ex.Message, "Eroare Ștergere", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                }
            }
        }

        //functii de validare 
        // pentru adaugare si actualizare
        private bool ValidateAdaugare()
        {
            if (tb_cnpFT.Text.Length != 13) { MessageBox.Show("CNP invalid!"); return false; }
            if (string.IsNullOrWhiteSpace(tb_numeFT.Text) || string.IsNullOrWhiteSpace(tb_prenumeFT.Text) ||
    string.IsNullOrWhiteSpace(tb_functieFT.Text))
            {
                MessageBox.Show("Toate câmpurile (nume, prenume, funcție) sunt obligatorii!");
                return false;
            }

            if (!decimal.TryParse(tb_salarFT.Text, out decimal s) || s < 0) { MessageBox.Show("Salariu invalid!"); return false; }
            if (!decimal.TryParse(tb_bonusuriFT.Text, out decimal b) || b < 0)
            {
                MessageBox.Show("Bonusul nu poate fi negativ!");
                return false;
            }
            return true;
        }

        private bool ValidateUpdate()
        {
            if (string.IsNullOrWhiteSpace(tb_nume.Text) || string.IsNullOrWhiteSpace(tb_prenumeFT.Text) ||
    string.IsNullOrWhiteSpace(tb_functieFT.Text))
            {
                MessageBox.Show("Toate câmpurile (nume, prenume, funcție) sunt obligatorii!");
                return false;
            }

            if (!decimal.TryParse(tb_salar.Text, out _)) return false;
            return true;
        }
    }

    
=======
﻿using Microsoft.Data.SqlClient;
using System;
using System.Collections.Generic;
using System.Data;
using System.Windows.Forms;

namespace SGBD_lab1
{
    public partial class Form1 : Form
    {
        private DatabaseService dbService = new DatabaseService();
        private DataSet dataSet = new DataSet();
        private BindingSource bsParent = new BindingSource();
        private BindingSource bsChild = new BindingSource();

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            LoadData();
        }

        //incarcare date
        private void LoadData()
        {
            try
            {
                using (SqlConnection connection = new SqlConnection(dbService.ConnectionString))
                {
                    connection.Open();

                    SqlDataAdapter parentAdapter = new SqlDataAdapter("SELECT * FROM Firma_transport", connection);
                    SqlDataAdapter childAdapter = new SqlDataAdapter("SELECT * FROM Angajati", connection);

                    dataSet.Clear();
                    if (dataSet.Relations.Contains("FK_Firma_transport_Angajati"))
                        dataSet.Relations.Remove("FK_Firma_transport_Angajati");

                    parentAdapter.Fill(dataSet, "Firma_transport");
                    childAdapter.Fill(dataSet, "Angajati");

                    DataColumn pkColumn = dataSet.Tables["Firma_transport"].Columns["caen"];
                    DataColumn fkColumn = dataSet.Tables["Angajati"].Columns["caen"];

                    // stabilire relație 1-n  
                    DataRelation relation = new DataRelation("FK_Firma_transport_Angajati", pkColumn, fkColumn);
                    dataSet.Relations.Add(relation);

                    bsParent.DataSource = dataSet.Tables["Firma_transport"];
                    FIrma_DGW.DataSource = bsParent;

                    bsChild.DataSource = bsParent;
                    bsChild.DataMember = "FK_Firma_transport_Angajati";
                    Angajati_DGW.DataSource = bsChild;

                    // DataBinding pentru editare ușoară
                    ClearBindings();
                    tb_caen.DataBindings.Add("Text", bsChild, "caen", true);
                    tb_nume.DataBindings.Add("Text", bsChild, "nume", true);
                    tb_prenume.DataBindings.Add("Text", bsChild, "prenume", true);
                    tb_functie.DataBindings.Add("Text", bsChild, "functie", true);
                    tb_salar.DataBindings.Add("Text", bsChild, "salar", true);
                    tb_bonusuri.DataBindings.Add("Text", bsChild, "bonusuri", true);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Eroare la încărcare: " + ex.Message);
            }
        }

        private void ClearBindings()
        {
            tb_caen.DataBindings.Clear();
            tb_nume.DataBindings.Clear();
            tb_prenume.DataBindings.Clear();
            tb_functie.DataBindings.Clear();
            tb_salar.DataBindings.Clear();
            tb_bonusuri.DataBindings.Clear();
        }

        //buton refresh
        private void btn_refresh_Click(object sender, EventArgs e)
        {
            LoadData(); 
            MessageBox.Show("Date reîncărcate cu succes!");
        }

        //buton adaugare
        private void btn_Add_Click(object sender, EventArgs e)
        {
            //   selectam firma
            if (FIrma_DGW.CurrentRow != null && ValidateAdaugare())
            {
                try
                {
                    // preluam caen de la randul cuurent
                    string caen = FIrma_DGW.CurrentRow.Cells["caen"].Value.ToString();
                    string query = "INSERT INTO Angajati(cnp, caen, nume, prenume, functie, salar, bonusuri) VALUES (@cnp, @caen, @nume, @prenume, @functie, @salar, @bonusuri)";

                    var parameters = new List<SqlParameter>
            {
                new SqlParameter("@cnp", tb_cnpFT.Text),
                new SqlParameter("@caen", caen),
                new SqlParameter("@nume", tb_numeFT.Text),
                new SqlParameter("@prenume", tb_prenumeFT.Text),
                new SqlParameter("@functie", tb_functieFT.Text),
                new SqlParameter("@salar", decimal.Parse(tb_salarFT.Text)),
                new SqlParameter("@bonusuri", decimal.Parse(tb_bonusuriFT.Text))
            };
                    dbService.ExecuteNonQuery(query, parameters);

                    tb_cnpFT.Clear();
                    tb_numeFT.Clear();
                    tb_prenumeFT.Clear();
                    tb_functieFT.Clear();
                    tb_salarFT.Clear();
                    tb_bonusuriFT.Clear();
                    LoadData();
                    MessageBox.Show("Angajat adăugat cu succes!");
                }
                catch (Exception ex)
                {
                    MessageBox.Show("Eroare la adăugare: " + ex.Message);
                }
            }
            else
            {
                MessageBox.Show("Vă rugăm să selectați o firmă și să completați corect datele!");
            }
        }

        //buton actualizare
        private void btn_Update_Click(object sender, EventArgs e)
        {
            // vf. daca exista un rand selectat 
            if (Angajati_DGW.CurrentRow != null)
            {
                if (ValidateUpdate())
                {
                    try
                    {
                        string cnp = Angajati_DGW.CurrentRow.Cells["cnp"].Value.ToString();
                        string query = "UPDATE Angajati SET nume=@nume, prenume=@prenume, functie=@functie, salar=@salar, bonusuri=@bonusuri WHERE cnp=@cnp";

                        var parameters = new List<SqlParameter>
                {
                    new SqlParameter("@nume", tb_nume.Text),
                    new SqlParameter("@prenume", tb_prenume.Text),
                    new SqlParameter("@functie", tb_functie.Text),
                    new SqlParameter("@salar", decimal.Parse(tb_salar.Text)),
                    new SqlParameter("@bonusuri", decimal.Parse(tb_bonusuri.Text)),
                    new SqlParameter("@cnp", cnp)
                };

                        dbService.ExecuteNonQuery(query, parameters);
                        LoadData();
                        MessageBox.Show("Actualizare realizata cu succes!", "Succes", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show("Eroare la baza de date: " + ex.Message, "Eroare", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                }
            }
            else
            {
                MessageBox.Show("Vă rugăm să selectați angajatul pe care doriți să îl modificați din tabel!", "Atenție", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }

        private void btn_Delete_Click(object sender, EventArgs e)
        {
            if (Angajati_DGW.SelectedRows.Count == 1)
            {
                if (MessageBox.Show("Sigur ștergeți acest angajat?", "Confirmare", MessageBoxButtons.YesNo) == DialogResult.Yes)
                {
                    try
                    {
                        string cnp = Angajati_DGW.SelectedRows[0].Cells["cnp"].Value.ToString();
                        string query = "DELETE FROM Angajati WHERE cnp = @cnp";
                        var parameters = new List<SqlParameter> { new SqlParameter("@cnp", cnp) };
                        dbService.ExecuteNonQuery(query, parameters);
                        LoadData();
                        MessageBox.Show("Angajat șters!");
                    }
                    catch (SqlException ex)
                    {
                        MessageBox.Show("Eroare bază de date: " + ex.Message, "Eroare Ștergere", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                }
            }
        }

        //functii de validare 
        // pentru adaugare si actualizare
        private bool ValidateAdaugare()
        {
            if (tb_cnpFT.Text.Length != 13) { MessageBox.Show("CNP invalid!"); return false; }
            if (string.IsNullOrWhiteSpace(tb_numeFT.Text) || string.IsNullOrWhiteSpace(tb_prenumeFT.Text) ||
    string.IsNullOrWhiteSpace(tb_functieFT.Text))
            {
                MessageBox.Show("Toate câmpurile (nume, prenume, funcție) sunt obligatorii!");
                return false;
            }

            if (!decimal.TryParse(tb_salarFT.Text, out decimal s) || s < 0) { MessageBox.Show("Salariu invalid!"); return false; }
            if (!decimal.TryParse(tb_bonusuriFT.Text, out decimal b) || b < 0)
            {
                MessageBox.Show("Bonusul nu poate fi negativ!");
                return false;
            }
            return true;
        }

        private bool ValidateUpdate()
        {
            if (string.IsNullOrWhiteSpace(tb_nume.Text) || string.IsNullOrWhiteSpace(tb_prenumeFT.Text) ||
    string.IsNullOrWhiteSpace(tb_functieFT.Text))
            {
                MessageBox.Show("Toate câmpurile (nume, prenume, funcție) sunt obligatorii!");
                return false;
            }

            if (!decimal.TryParse(tb_salar.Text, out _)) return false;
            return true;
        }
    }

    
>>>>>>> Stashed changes
}