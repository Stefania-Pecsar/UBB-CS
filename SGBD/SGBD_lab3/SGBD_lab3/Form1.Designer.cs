namespace SGBD_lab3
{
    partial class Form1
    {
        private System.ComponentModel.IContainer components = null;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        private void InitializeComponent()
        {
            this.dgvParinte = new System.Windows.Forms.DataGridView();
            this.dgvCopil = new System.Windows.Forms.DataGridView();
            this.txtCnp = new System.Windows.Forms.TextBox();
            this.txtNume = new System.Windows.Forms.TextBox();
            this.txtPrenume = new System.Windows.Forms.TextBox();
            this.txtFunctie = new System.Windows.Forms.TextBox();
            this.txtSalar = new System.Windows.Forms.TextBox();
            this.btnAdauga = new System.Windows.Forms.Button();
            this.btnModifica = new System.Windows.Forms.Button();
            this.btnSterge = new System.Windows.Forms.Button();
            this.btnTestA = new System.Windows.Forms.Button();
            this.btnTestB = new System.Windows.Forms.Button();
            this.btnTestB_Fixed = new System.Windows.Forms.Button();
            this.btnLazyEager = new System.Windows.Forms.Button();
            this.lblParinte = new System.Windows.Forms.Label();
            this.lblCopil = new System.Windows.Forms.Label();
            this.lblCnp = new System.Windows.Forms.Label();
            this.lblNume = new System.Windows.Forms.Label();
            this.lblPrenume = new System.Windows.Forms.Label();
            this.lblFunctie = new System.Windows.Forms.Label();
            this.lblSalar = new System.Windows.Forms.Label();
            this.btnN1 = new System.Windows.Forms.Button();
            this.btnIndex = new System.Windows.Forms.Button();
            this.btnPaginare = new System.Windows.Forms.Button();
            this.btnCache = new System.Windows.Forms.Button();
            this.btnBulk = new System.Windows.Forms.Button();
            this.btnPreparedStatements = new System.Windows.Forms.Button();
            this.btnPrev = new System.Windows.Forms.Button();
            this.btnNext = new System.Windows.Forms.Button();
            this.lblPagina = new System.Windows.Forms.Label();
            this.lblTotal = new System.Windows.Forms.Label();
            this.cmbPageSize = new System.Windows.Forms.ComboBox();
            this.lblSize = new System.Windows.Forms.Label();
            this.rbOffset = new System.Windows.Forms.RadioButton();
            this.rbKeyset = new System.Windows.Forms.RadioButton();
            this.btnGenereazaDate = new System.Windows.Forms.Button();
            this.btnExplain = new System.Windows.Forms.Button();

            // Lab 5 – controale pentru soft delete
            this.chkVeziSterse = new System.Windows.Forms.CheckBox();
            this.btnRestaureaza = new System.Windows.Forms.Button();
            ((System.ComponentModel.ISupportInitialize)(this.dgvParinte)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.dgvCopil)).BeginInit();
            this.SuspendLayout();
            // 
            // dgvParinte
            // 
            this.dgvParinte.AllowUserToAddRows = false;
            this.dgvParinte.AllowUserToDeleteRows = false;
            this.dgvParinte.AutoSizeColumnsMode = System.Windows.Forms.DataGridViewAutoSizeColumnsMode.Fill;
            this.dgvParinte.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dgvParinte.Location = new System.Drawing.Point(12, 27);
            this.dgvParinte.Name = "dgvParinte";
            this.dgvParinte.ReadOnly = true;
            this.dgvParinte.SelectionMode = System.Windows.Forms.DataGridViewSelectionMode.FullRowSelect;
            this.dgvParinte.Size = new System.Drawing.Size(760, 130);
            this.dgvParinte.TabIndex = 0;
            // 
            // dgvCopil
            // 
            this.dgvCopil.AllowUserToAddRows = false;
            this.dgvCopil.AllowUserToDeleteRows = false;
            this.dgvCopil.AutoSizeColumnsMode = System.Windows.Forms.DataGridViewAutoSizeColumnsMode.Fill;
            this.dgvCopil.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dgvCopil.Location = new System.Drawing.Point(12, 180);
            this.dgvCopil.Name = "dgvCopil";
            this.dgvCopil.ReadOnly = true;
            this.dgvCopil.SelectionMode = System.Windows.Forms.DataGridViewSelectionMode.FullRowSelect;
            this.dgvCopil.Size = new System.Drawing.Size(760, 130);
            this.dgvCopil.TabIndex = 1;
            // 
            // txtCnp
            // 
            this.txtCnp.Location = new System.Drawing.Point(12, 385);
            this.txtCnp.Name = "txtCnp";
            this.txtCnp.Size = new System.Drawing.Size(100, 23);
            this.txtCnp.TabIndex = 2;
            // 
            // txtNume
            // 
            this.txtNume.Location = new System.Drawing.Point(120, 385);
            this.txtNume.Name = "txtNume";
            this.txtNume.Size = new System.Drawing.Size(100, 23);
            this.txtNume.TabIndex = 3;
            // 
            // txtPrenume
            // 
            this.txtPrenume.Location = new System.Drawing.Point(230, 385);
            this.txtPrenume.Name = "txtPrenume";
            this.txtPrenume.Size = new System.Drawing.Size(100, 23);
            this.txtPrenume.TabIndex = 4;
            // 
            // txtFunctie
            // 
            this.txtFunctie.Location = new System.Drawing.Point(340, 385);
            this.txtFunctie.Name = "txtFunctie";
            this.txtFunctie.Size = new System.Drawing.Size(100, 23);
            this.txtFunctie.TabIndex = 5;
            // 
            // txtSalar
            // 
            this.txtSalar.Location = new System.Drawing.Point(450, 385);
            this.txtSalar.Name = "txtSalar";
            this.txtSalar.Size = new System.Drawing.Size(100, 23);
            this.txtSalar.TabIndex = 6;
            // 
            // btnAdauga
            // 
            this.btnAdauga.Location = new System.Drawing.Point(12, 415);
            this.btnAdauga.Name = "btnAdauga";
            this.btnAdauga.Size = new System.Drawing.Size(100, 30);
            this.btnAdauga.TabIndex = 7;
            this.btnAdauga.Text = "Adaugă";
            this.btnAdauga.UseVisualStyleBackColor = true;
            // 
            // btnModifica
            // 
            this.btnModifica.Location = new System.Drawing.Point(120, 415);
            this.btnModifica.Name = "btnModifica";
            this.btnModifica.Size = new System.Drawing.Size(100, 30);
            this.btnModifica.TabIndex = 8;
            this.btnModifica.Text = "Modifică";
            this.btnModifica.UseVisualStyleBackColor = true;
            // 
            // btnSterge
            // 
            this.btnSterge.Location = new System.Drawing.Point(230, 415);
            this.btnSterge.Name = "btnSterge";
            this.btnSterge.Size = new System.Drawing.Size(100, 30);
            this.btnSterge.TabIndex = 9;
            this.btnSterge.Text = "Șterge";
            this.btnSterge.UseVisualStyleBackColor = true;
            // 
            // btnTestA
            // 
            this.btnTestA.BackColor = System.Drawing.Color.LightSkyBlue;
            this.btnTestA.Location = new System.Drawing.Point(340, 415);
            this.btnTestA.Name = "btnTestA";
            this.btnTestA.Size = new System.Drawing.Size(150, 30);
            this.btnTestA.TabIndex = 10;
            this.btnTestA.Text = "Test A: Pooling";
            this.btnTestA.UseVisualStyleBackColor = false;
            // 
            // btnTestB
            // 
            this.btnTestB.BackColor = System.Drawing.Color.LightCoral;
            this.btnTestB.Location = new System.Drawing.Point(500, 415);
            this.btnTestB.Name = "btnTestB";
            this.btnTestB.Size = new System.Drawing.Size(150, 30);
            this.btnTestB.TabIndex = 11;
            this.btnTestB.Text = "Test B: Leak";
            this.btnTestB.UseVisualStyleBackColor = false;
            // 
            // btnTestB_Fixed
            // 
            this.btnTestB_Fixed.BackColor = System.Drawing.Color.LightGreen;
            this.btnTestB_Fixed.Location = new System.Drawing.Point(12, 451);
            this.btnTestB_Fixed.Name = "btnTestB_Fixed";
            this.btnTestB_Fixed.Size = new System.Drawing.Size(150, 30);
            this.btnTestB_Fixed.TabIndex = 12;
            this.btnTestB_Fixed.Text = "Test B Fixed (No Leak)";
            this.btnTestB_Fixed.UseVisualStyleBackColor = false;
            // 
            // btnLazyEager
            // 
            this.btnLazyEager.BackColor = System.Drawing.Color.LightGoldenrodYellow;
            this.btnLazyEager.Location = new System.Drawing.Point(170, 451);
            this.btnLazyEager.Name = "btnLazyEager";
            this.btnLazyEager.Size = new System.Drawing.Size(150, 30);
            this.btnLazyEager.TabIndex = 13;
            this.btnLazyEager.Text = "Lazy vs Eager Loading";
            this.btnLazyEager.UseVisualStyleBackColor = false;
            // 
            // lblParinte
            // 
            this.lblParinte.AutoSize = true;
            this.lblParinte.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point);
            this.lblParinte.Location = new System.Drawing.Point(12, 9);
            this.lblParinte.Name = "lblParinte";
            this.lblParinte.Size = new System.Drawing.Size(183, 15);
            this.lblParinte.TabIndex = 14;
            this.lblParinte.Text = "Tabel Părinte (Firme Transport)";
            // 
            // lblCopil
            // 
            this.lblCopil.AutoSize = true;
            this.lblCopil.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point);
            this.lblCopil.Location = new System.Drawing.Point(12, 162);
            this.lblCopil.Name = "lblCopil";
            this.lblCopil.Size = new System.Drawing.Size(125, 15);
            this.lblCopil.TabIndex = 15;
            this.lblCopil.Text = "Tabel Copil (Angajați)";
            // 
            // lblCnp
            // 
            this.lblCnp.AutoSize = true;
            this.lblCnp.Location = new System.Drawing.Point(12, 367);
            this.lblCnp.Name = "lblCnp";
            this.lblCnp.Size = new System.Drawing.Size(34, 15);
            this.lblCnp.TabIndex = 16;
            this.lblCnp.Text = "CNP:";
            // 
            // lblNume
            // 
            this.lblNume.AutoSize = true;
            this.lblNume.Location = new System.Drawing.Point(120, 367);
            this.lblNume.Name = "lblNume";
            this.lblNume.Size = new System.Drawing.Size(43, 15);
            this.lblNume.TabIndex = 17;
            this.lblNume.Text = "Nume:";
            // 
            // lblPrenume
            // 
            this.lblPrenume.AutoSize = true;
            this.lblPrenume.Location = new System.Drawing.Point(230, 367);
            this.lblPrenume.Name = "lblPrenume";
            this.lblPrenume.Size = new System.Drawing.Size(57, 15);
            this.lblPrenume.TabIndex = 18;
            this.lblPrenume.Text = "Prenume:";
            // 
            // lblFunctie
            // 
            this.lblFunctie.AutoSize = true;
            this.lblFunctie.Location = new System.Drawing.Point(340, 367);
            this.lblFunctie.Name = "lblFunctie";
            this.lblFunctie.Size = new System.Drawing.Size(49, 15);
            this.lblFunctie.TabIndex = 19;
            this.lblFunctie.Text = "Funcție:";
            // 
            // lblSalar
            // 
            this.lblSalar.AutoSize = true;
            this.lblSalar.Location = new System.Drawing.Point(450, 367);
            this.lblSalar.Name = "lblSalar";
            this.lblSalar.Size = new System.Drawing.Size(35, 15);
            this.lblSalar.TabIndex = 20;
            this.lblSalar.Text = "Salar:";
            // 
            // btnN1
            // 
            this.btnN1.BackColor = System.Drawing.Color.LightCyan;
            this.btnN1.Location = new System.Drawing.Point(12, 513);
            this.btnN1.Name = "btnN1";
            this.btnN1.Size = new System.Drawing.Size(120, 35);
            this.btnN1.TabIndex = 21;
            this.btnN1.Text = "Lab4: N+1";
            this.btnN1.UseVisualStyleBackColor = false;
            // 
            // btnIndex
            // 
            this.btnIndex.BackColor = System.Drawing.Color.LightCyan;
            this.btnIndex.Location = new System.Drawing.Point(140, 513);
            this.btnIndex.Name = "btnIndex";
            this.btnIndex.Size = new System.Drawing.Size(120, 35);
            this.btnIndex.TabIndex = 22;
            this.btnIndex.Text = "Lab4: Index Bench";
            this.btnIndex.UseVisualStyleBackColor = false;
            // 
            // btnPaginare
            // 
            this.btnPaginare.BackColor = System.Drawing.Color.LightCyan;
            this.btnPaginare.Location = new System.Drawing.Point(270, 513);
            this.btnPaginare.Name = "btnPaginare";
            this.btnPaginare.Size = new System.Drawing.Size(120, 35);
            this.btnPaginare.TabIndex = 23;
            this.btnPaginare.Text = "Lab4: Paginare Bnch";
            this.btnPaginare.UseVisualStyleBackColor = false;
            // 
            // btnCache
            // 
            this.btnCache.BackColor = System.Drawing.Color.LightCyan;
            this.btnCache.Location = new System.Drawing.Point(400, 513);
            this.btnCache.Name = "btnCache";
            this.btnCache.Size = new System.Drawing.Size(120, 35);
            this.btnCache.TabIndex = 24;
            this.btnCache.Text = "Lab4: Caching";
            this.btnCache.UseVisualStyleBackColor = false;
            // 
            // btnBulk
            // 
            this.btnBulk.BackColor = System.Drawing.Color.LightCyan;
            this.btnBulk.Location = new System.Drawing.Point(530, 513);
            this.btnBulk.Name = "btnBulk";
            this.btnBulk.Size = new System.Drawing.Size(120, 35);
            this.btnBulk.TabIndex = 25;
            this.btnBulk.Text = "Lab4: Bulk Update";
            this.btnBulk.UseVisualStyleBackColor = false;
            // 
            // btnPreparedStatements
            // 
            this.btnPreparedStatements.BackColor = System.Drawing.Color.LightCyan;
            this.btnPreparedStatements.Location = new System.Drawing.Point(660, 513);
            this.btnPreparedStatements.Name = "btnPreparedStatements";
            this.btnPreparedStatements.Size = new System.Drawing.Size(112, 35);
            this.btnPreparedStatements.TabIndex = 26;
            this.btnPreparedStatements.Text = "Lab4: PrepStmt";
            this.btnPreparedStatements.UseVisualStyleBackColor = false;
            // 
            // btnPrev
            // 
            this.btnPrev.Location = new System.Drawing.Point(12, 316);
            this.btnPrev.Name = "btnPrev";
            this.btnPrev.Size = new System.Drawing.Size(75, 23);
            this.btnPrev.TabIndex = 27;
            this.btnPrev.Text = "< Anterior";
            this.btnPrev.UseVisualStyleBackColor = true;
            // 
            // btnNext
            // 
            this.btnNext.Location = new System.Drawing.Point(90, 316);
            this.btnNext.Name = "btnNext";
            this.btnNext.Size = new System.Drawing.Size(75, 23);
            this.btnNext.TabIndex = 28;
            this.btnNext.Text = "Următor >";
            this.btnNext.UseVisualStyleBackColor = true;
            // 
            // lblPagina
            // 
            this.lblPagina.AutoSize = true;
            this.lblPagina.Location = new System.Drawing.Point(180, 320);
            this.lblPagina.Name = "lblPagina";
            this.lblPagina.Size = new System.Drawing.Size(55, 15);
            this.lblPagina.TabIndex = 29;
            this.lblPagina.Text = "Pagina: 1";
            // 
            // lblTotal
            // 
            this.lblTotal.AutoSize = true;
            this.lblTotal.Location = new System.Drawing.Point(280, 320);
            this.lblTotal.Name = "lblTotal";
            this.lblTotal.Size = new System.Drawing.Size(45, 15);
            this.lblTotal.TabIndex = 30;
            this.lblTotal.Text = "Total: 0";
            // 
            // cmbPageSize
            // 
            this.cmbPageSize.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.cmbPageSize.FormattingEnabled = true;
            this.cmbPageSize.Items.AddRange(new object[] {
            "10",
            "25",
            "50",
            "100"});
            this.cmbPageSize.Location = new System.Drawing.Point(640, 316);
            this.cmbPageSize.Name = "cmbPageSize";
            this.cmbPageSize.Size = new System.Drawing.Size(132, 23);
            this.cmbPageSize.TabIndex = 31;
            // 
            // lblSize
            // 
            this.lblSize.AutoSize = true;
            this.lblSize.Location = new System.Drawing.Point(600, 320);
            this.lblSize.Name = "lblSize";
            this.lblSize.Size = new System.Drawing.Size(30, 15);
            this.lblSize.TabIndex = 32;
            this.lblSize.Text = "Size:";
            // 
            // rbOffset
            // 
            this.rbOffset.AutoSize = true;
            this.rbOffset.Checked = true;
            this.rbOffset.Location = new System.Drawing.Point(12, 345);
            this.rbOffset.Name = "rbOffset";
            this.rbOffset.Size = new System.Drawing.Size(107, 19);
            this.rbOffset.TabIndex = 33;
            this.rbOffset.TabStop = true;
            this.rbOffset.Text = "Paginare Offset";
            this.rbOffset.UseVisualStyleBackColor = true;
            // 
            // rbKeyset
            // 
            this.rbKeyset.AutoSize = true;
            this.rbKeyset.Location = new System.Drawing.Point(130, 345);
            this.rbKeyset.Name = "rbKeyset";
            this.rbKeyset.Size = new System.Drawing.Size(109, 19);
            this.rbKeyset.TabIndex = 34;
            this.rbKeyset.Text = "Paginare Keyset";
            this.rbKeyset.UseVisualStyleBackColor = true;
            // 
            // btnGenereazaDate
            // 
            this.btnGenereazaDate.Location = new System.Drawing.Point(340, 451);
            this.btnGenereazaDate.Name = "btnGenereazaDate";
            this.btnGenereazaDate.Size = new System.Drawing.Size(150, 30);
            this.btnGenereazaDate.TabIndex = 35;
            this.btnGenereazaDate.Text = "Generează 10k Date";
            this.btnGenereazaDate.UseVisualStyleBackColor = true;
            this.btnGenereazaDate.Click += new System.EventHandler(this.BtnGenereazaDate_Click);
            // 
            // btnExplain
            // 
            this.btnExplain.Location = new System.Drawing.Point(500, 451);
            this.btnExplain.Name = "btnExplain";
            this.btnExplain.Size = new System.Drawing.Size(150, 30);
            this.btnExplain.TabIndex = 36;
            this.btnExplain.Text = "Explain Analyze";
            this.btnExplain.UseVisualStyleBackColor = true;
            this.btnExplain.Click += new System.EventHandler(this.BtnExplain_Click);
            // 
            // chkVeziSterse
            // 
            this.chkVeziSterse.AutoSize = true;
            this.chkVeziSterse.Location = new System.Drawing.Point(660, 345);
            this.chkVeziSterse.Name = "chkVeziSterse";
            this.chkVeziSterse.Size = new System.Drawing.Size(98, 19);
            this.chkVeziSterse.TabIndex = 37;
            this.chkVeziSterse.Text = "Arată doar șterși";
            this.chkVeziSterse.UseVisualStyleBackColor = true;
            this.chkVeziSterse.CheckedChanged += new System.EventHandler(this.chkVeziSterse_CheckedChanged);
            // 
            // btnRestaureaza
            // 
            this.btnRestaureaza.Location = new System.Drawing.Point(660, 415);
            this.btnRestaureaza.Name = "btnRestaureaza";
            this.btnRestaureaza.Size = new System.Drawing.Size(100, 30);
            this.btnRestaureaza.TabIndex = 38;
            this.btnRestaureaza.Text = "Restaurează";
            this.btnRestaureaza.UseVisualStyleBackColor = true;
            this.btnRestaureaza.Click += new System.EventHandler(this.btnRestaureaza_Click);

            this.btnTestLocking = new System.Windows.Forms.Button();
            this.btnTestLocking.Location = new System.Drawing.Point(660, 451);
            this.btnTestLocking.Size = new System.Drawing.Size(120, 30);
            this.btnTestLocking.Text = "🔒 Test Locking";
            this.btnTestLocking.UseVisualStyleBackColor = true;
            this.btnTestLocking.Click += new System.EventHandler(this.BtnTestLocking_Click);
            this.Controls.Add(this.btnTestLocking);

            // Controale pentru căutare
            this.lblCautare = new System.Windows.Forms.Label();
            this.txtCautareCnp = new System.Windows.Forms.TextBox();
            this.btnCauta = new System.Windows.Forms.Button();
            this.lblStareAngajat = new System.Windows.Forms.Label();

            // lblCautare
            this.lblCautare.AutoSize = true;
            this.lblCautare.Location = new System.Drawing.Point(12, 490);
            this.lblCautare.Name = "lblCautare";
            this.lblCautare.Size = new System.Drawing.Size(95, 15);
            this.lblCautare.TabIndex = 39;
            this.lblCautare.Text = "Caută după CNP:";

            // txtCautareCnp
            this.txtCautareCnp.Location = new System.Drawing.Point(110, 487);
            this.txtCautareCnp.Name = "txtCautareCnp";
            this.txtCautareCnp.Size = new System.Drawing.Size(150, 23);
            this.txtCautareCnp.TabIndex = 40;

            // btnCauta
            this.btnCauta.Location = new System.Drawing.Point(270, 487);
            this.btnCauta.Name = "btnCauta";
            this.btnCauta.Size = new System.Drawing.Size(75, 23);
            this.btnCauta.TabIndex = 41;
            this.btnCauta.Text = "Caută";
            this.btnCauta.UseVisualStyleBackColor = true;
            this.btnCauta.Click += new System.EventHandler(this.BtnCauta_Click);

            //btnsetergere
            this.btnStergePermanent = new System.Windows.Forms.Button();
            this.btnStergePermanent.Location = new System.Drawing.Point(700, 385); // ajustează poziția
            this.btnStergePermanent.Size = new System.Drawing.Size(100, 30);
            this.btnStergePermanent.Text = "Șterge permanent";
            this.btnStergePermanent.UseVisualStyleBackColor = true;
            this.btnStergePermanent.Click += new System.EventHandler(this.BtnStergePermanent_Click);
            this.Controls.Add(this.btnStergePermanent);

            // lblStareAngajat
            this.lblStareAngajat.AutoSize = true;
            this.lblStareAngajat.Location = new System.Drawing.Point(360, 490);
            this.lblStareAngajat.Name = "lblStareAngajat";
            this.lblStareAngajat.Size = new System.Drawing.Size(0, 15);
            this.lblStareAngajat.TabIndex = 42;

            // txtTelefon
            this.txtTelefon = new System.Windows.Forms.TextBox();
            this.lblTelefon = new System.Windows.Forms.Label();
            // 
            // txtTelefon
            // 
            this.txtTelefon.Location = new System.Drawing.Point(560, 385);
            this.txtTelefon.Name = "txtTelefon";
            this.txtTelefon.Size = new System.Drawing.Size(120, 23);
            this.txtTelefon.TabIndex = 7;
            // 
            // lblTelefon
            // 
            this.lblTelefon.AutoSize = true;
            this.lblTelefon.Location = new System.Drawing.Point(560, 367);
            this.lblTelefon.Name = "lblTelefon";
            this.lblTelefon.Size = new System.Drawing.Size(52, 15);
            this.lblTelefon.TabIndex = 21;
            this.lblTelefon.Text = "Telefon:";

            // btnArataProiecte
            this.btnArataProiecte = new System.Windows.Forms.Button();
            this.btnArataProiecte.Location = new System.Drawing.Point(660, 485);
            this.btnArataProiecte.Name = "btnArataProiecte";
            this.btnArataProiecte.Size = new System.Drawing.Size(120, 30);
            this.btnArataProiecte.TabIndex = 39;
            this.btnArataProiecte.Text = "Arată Proiecte";
            this.btnArataProiecte.UseVisualStyleBackColor = true;
            this.btnArataProiecte.Click += new System.EventHandler(this.btnArataProiecte_Click);

            // Adaugă controalele în formular (după btnExplain etc.)
            this.Controls.Add(this.lblCautare);
            this.Controls.Add(this.txtCautareCnp);
            this.Controls.Add(this.btnCauta);
            this.Controls.Add(this.lblStareAngajat);

            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(800, 564);
            this.Controls.Add(this.btnRestaureaza);
            this.Controls.Add(this.chkVeziSterse);
            this.Controls.Add(this.btnExplain);
            this.Controls.Add(this.btnGenereazaDate);
            this.Controls.Add(this.rbKeyset);
            this.Controls.Add(this.rbOffset);
            this.Controls.Add(this.lblSize);
            this.Controls.Add(this.cmbPageSize);
            this.Controls.Add(this.lblTotal);
            this.Controls.Add(this.lblPagina);
            this.Controls.Add(this.btnNext);
            this.Controls.Add(this.btnPrev);
            this.Controls.Add(this.btnPreparedStatements);
            this.Controls.Add(this.btnBulk);
            this.Controls.Add(this.btnCache);
            this.Controls.Add(this.btnPaginare);
            this.Controls.Add(this.btnIndex);
            this.Controls.Add(this.btnN1);
            this.Controls.Add(this.lblSalar);
            this.Controls.Add(this.lblFunctie);
            this.Controls.Add(this.lblPrenume);
            this.Controls.Add(this.lblNume);
            this.Controls.Add(this.lblCnp);
            this.Controls.Add(this.lblCopil);
            this.Controls.Add(this.lblParinte);
            this.Controls.Add(this.btnLazyEager);
            this.Controls.Add(this.btnTestB_Fixed);
            this.Controls.Add(this.btnTestB);
            this.Controls.Add(this.btnTestA);
            this.Controls.Add(this.btnSterge);
            this.Controls.Add(this.btnModifica);
            this.Controls.Add(this.btnAdauga);
            this.Controls.Add(this.txtSalar);
            this.Controls.Add(this.txtFunctie);
            this.Controls.Add(this.txtPrenume);
            this.Controls.Add(this.txtNume);
            this.Controls.Add(this.txtCnp);
            this.Controls.Add(this.dgvCopil);
            this.Controls.Add(this.dgvParinte);
            this.Controls.Add(this.txtTelefon);
            this.Controls.Add(this.lblTelefon);
            this.Controls.Add(this.btnArataProiecte);
            this.Name = "Form1";
            this.Text = "SGBD Lab 3-5";
            ((System.ComponentModel.ISupportInitialize)(this.dgvParinte)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.dgvCopil)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();
        }

        #endregion

        private System.Windows.Forms.DataGridView dgvParinte;
        private System.Windows.Forms.DataGridView dgvCopil;
        private System.Windows.Forms.TextBox txtCnp;
        private System.Windows.Forms.TextBox txtNume;
        private System.Windows.Forms.TextBox txtPrenume;
        private System.Windows.Forms.TextBox txtFunctie;
        private System.Windows.Forms.TextBox txtSalar;
        private System.Windows.Forms.Button btnAdauga;
        private System.Windows.Forms.Button btnModifica;
        private System.Windows.Forms.Button btnSterge;
        private System.Windows.Forms.Button btnTestA;
        private System.Windows.Forms.Button btnTestB;
        private System.Windows.Forms.Button btnTestB_Fixed;
        private System.Windows.Forms.Button btnLazyEager;
        private System.Windows.Forms.Label lblParinte;
        private System.Windows.Forms.Label lblCopil;
        private System.Windows.Forms.Label lblCnp;
        private System.Windows.Forms.Label lblNume;
        private System.Windows.Forms.Label lblPrenume;
        private System.Windows.Forms.Label lblFunctie;
        private System.Windows.Forms.Label lblSalar;
        private System.Windows.Forms.Button btnN1;
        private System.Windows.Forms.Button btnIndex;
        private System.Windows.Forms.Button btnPaginare;
        private System.Windows.Forms.Button btnCache;
        private System.Windows.Forms.Button btnBulk;
        private System.Windows.Forms.Button btnPreparedStatements;
        private System.Windows.Forms.Button btnPrev;
        private System.Windows.Forms.Button btnNext;
        private System.Windows.Forms.Label lblPagina;
        private System.Windows.Forms.Label lblTotal;
        private System.Windows.Forms.ComboBox cmbPageSize;
        private System.Windows.Forms.Label lblSize;
        private System.Windows.Forms.RadioButton rbOffset;
        private System.Windows.Forms.RadioButton rbKeyset;
        private System.Windows.Forms.Button btnGenereazaDate;
        private System.Windows.Forms.Button btnExplain;
        private System.Windows.Forms.Label lblCautare;
        private System.Windows.Forms.TextBox txtCautareCnp;
        private System.Windows.Forms.Button btnCauta;
        private System.Windows.Forms.Label lblStareAngajat;
        private System.Windows.Forms.CheckBox chkVeziSterse;
        private System.Windows.Forms.Button btnRestaureaza;
        private System.Windows.Forms.Button btnTestLocking;
        private System.Windows.Forms.Button btnStergePermanent;
        private System.Windows.Forms.TextBox txtTelefon;
        private System.Windows.Forms.Label lblTelefon;
        private System.Windows.Forms.Button btnArataProiecte;
    }
}