namespace SGBD_Lab2
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
            this.rtbLogs = new System.Windows.Forms.RichTextBox();
            this.btnDirtyReadProblem = new System.Windows.Forms.Button();
            this.btnDirtyReadSolved = new System.Windows.Forms.Button();
            this.btnNonRepeatableProblem = new System.Windows.Forms.Button();
            this.btnNonRepeatableSolved = new System.Windows.Forms.Button();
            this.btnPhantomProblem = new System.Windows.Forms.Button();
            this.btnPhantomSolved = new System.Windows.Forms.Button();
            this.btnLostUpdateProblem = new System.Windows.Forms.Button();
            this.btnLostUpdateSolved = new System.Windows.Forms.Button();
            this.btnDeadlockProblem = new System.Windows.Forms.Button();
            this.btnDeadlockSolved = new System.Windows.Forms.Button();
            this.btnTestBatch = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // rtbLogs
            // 
            this.rtbLogs.Font = new System.Drawing.Font("Consolas", 10.2F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point);
            this.rtbLogs.Location = new System.Drawing.Point(313, 12);
            this.rtbLogs.Name = "rtbLogs";
            this.rtbLogs.ReadOnly = true;
            this.rtbLogs.Size = new System.Drawing.Size(650, 545);
            this.rtbLogs.TabIndex = 0;
            this.rtbLogs.Text = "";
            // 
            // btnDirtyReadProblem
            // 
            this.btnDirtyReadProblem.Location = new System.Drawing.Point(12, 12);
            this.btnDirtyReadProblem.Name = "btnDirtyReadProblem";
            this.btnDirtyReadProblem.Size = new System.Drawing.Size(280, 40);
            this.btnDirtyReadProblem.TabIndex = 1;
            this.btnDirtyReadProblem.Text = "1. Dirty Read (Apare)";
            this.btnDirtyReadProblem.UseVisualStyleBackColor = true;
            this.btnDirtyReadProblem.Click += new System.EventHandler(this.btnDirtyReadProblem_Click);
            // 
            // btnDirtyReadSolved
            // 
            this.btnDirtyReadSolved.Location = new System.Drawing.Point(12, 58);
            this.btnDirtyReadSolved.Name = "btnDirtyReadSolved";
            this.btnDirtyReadSolved.Size = new System.Drawing.Size(280, 40);
            this.btnDirtyReadSolved.TabIndex = 2;
            this.btnDirtyReadSolved.Text = "1. Dirty Read (Prevenita)";
            this.btnDirtyReadSolved.UseVisualStyleBackColor = true;
            this.btnDirtyReadSolved.Click += new System.EventHandler(this.btnDirtyReadSolved_Click);
            // 
            // btnNonRepeatableProblem
            // 
            this.btnNonRepeatableProblem.Location = new System.Drawing.Point(12, 104);
            this.btnNonRepeatableProblem.Name = "btnNonRepeatableProblem";
            this.btnNonRepeatableProblem.Size = new System.Drawing.Size(280, 40);
            this.btnNonRepeatableProblem.TabIndex = 3;
            this.btnNonRepeatableProblem.Text = "2. Non-Repeatable (Apare)";
            this.btnNonRepeatableProblem.UseVisualStyleBackColor = true;
            this.btnNonRepeatableProblem.Click += new System.EventHandler(this.btnNonRepeatableProblem_Click);
            // 
            // btnNonRepeatableSolved
            // 
            this.btnNonRepeatableSolved.Location = new System.Drawing.Point(12, 150);
            this.btnNonRepeatableSolved.Name = "btnNonRepeatableSolved";
            this.btnNonRepeatableSolved.Size = new System.Drawing.Size(280, 40);
            this.btnNonRepeatableSolved.TabIndex = 4;
            this.btnNonRepeatableSolved.Text = "2. Non-Repeatable (Prevenita)";
            this.btnNonRepeatableSolved.UseVisualStyleBackColor = true;
            this.btnNonRepeatableSolved.Click += new System.EventHandler(this.btnNonRepeatableSolved_Click);
            // 
            // btnPhantomProblem
            // 
            this.btnPhantomProblem.Location = new System.Drawing.Point(12, 196);
            this.btnPhantomProblem.Name = "btnPhantomProblem";
            this.btnPhantomProblem.Size = new System.Drawing.Size(280, 40);
            this.btnPhantomProblem.TabIndex = 5;
            this.btnPhantomProblem.Text = "3. Phantom Read (Apare)";
            this.btnPhantomProblem.UseVisualStyleBackColor = true;
            this.btnPhantomProblem.Click += new System.EventHandler(this.btnPhantomProblem_Click);
            // 
            // btnPhantomSolved
            // 
            this.btnPhantomSolved.Location = new System.Drawing.Point(12, 242);
            this.btnPhantomSolved.Name = "btnPhantomSolved";
            this.btnPhantomSolved.Size = new System.Drawing.Size(280, 40);
            this.btnPhantomSolved.TabIndex = 6;
            this.btnPhantomSolved.Text = "3. Phantom Read (Prevenita)";
            this.btnPhantomSolved.UseVisualStyleBackColor = true;
            this.btnPhantomSolved.Click += new System.EventHandler(this.btnPhantomSolved_Click);
            // 
            // btnLostUpdateProblem
            // 
            this.btnLostUpdateProblem.Location = new System.Drawing.Point(12, 288);
            this.btnLostUpdateProblem.Name = "btnLostUpdateProblem";
            this.btnLostUpdateProblem.Size = new System.Drawing.Size(280, 40);
            this.btnLostUpdateProblem.TabIndex = 7;
            this.btnLostUpdateProblem.Text = "4. Lost Update (Apare)";
            this.btnLostUpdateProblem.UseVisualStyleBackColor = true;
            this.btnLostUpdateProblem.Click += new System.EventHandler(this.btnLostUpdateProblem_Click);
            // 
            // btnLostUpdateSolved
            // 
            this.btnLostUpdateSolved.Location = new System.Drawing.Point(12, 334);
            this.btnLostUpdateSolved.Name = "btnLostUpdateSolved";
            this.btnLostUpdateSolved.Size = new System.Drawing.Size(280, 40);
            this.btnLostUpdateSolved.TabIndex = 8;
            this.btnLostUpdateSolved.Text = "4. Lost Update (Prevenita)";
            this.btnLostUpdateSolved.UseVisualStyleBackColor = true;
            this.btnLostUpdateSolved.Click += new System.EventHandler(this.btnLostUpdateSolved_Click);
            // 
            // btnDeadlockProblem
            // 
            this.btnDeadlockProblem.Location = new System.Drawing.Point(12, 380);
            this.btnDeadlockProblem.Name = "btnDeadlockProblem";
            this.btnDeadlockProblem.Size = new System.Drawing.Size(280, 40);
            this.btnDeadlockProblem.TabIndex = 9;
            this.btnDeadlockProblem.Text = "5. Deadlock (Apare)";
            this.btnDeadlockProblem.UseVisualStyleBackColor = true;
            this.btnDeadlockProblem.Click += new System.EventHandler(this.btnDeadlockProblem_Click);
            // 
            // btnDeadlockSolved
            // 
            this.btnDeadlockSolved.Location = new System.Drawing.Point(12, 426);
            this.btnDeadlockSolved.Name = "btnDeadlockSolved";
            this.btnDeadlockSolved.Size = new System.Drawing.Size(280, 40);
            this.btnDeadlockSolved.TabIndex = 10;
            this.btnDeadlockSolved.Text = "5. Deadlock (Prevenita)";
            this.btnDeadlockSolved.UseVisualStyleBackColor = true;
            this.btnDeadlockSolved.Click += new System.EventHandler(this.btnDeadlockSolved_Click);
            // 
            // btnTestBatch
            // 
            this.btnTestBatch.BackColor = System.Drawing.Color.LightSkyBlue;
            this.btnTestBatch.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point);
            this.btnTestBatch.Location = new System.Drawing.Point(12, 490);
            this.btnTestBatch.Name = "btnTestBatch";
            this.btnTestBatch.Size = new System.Drawing.Size(280, 67);
            this.btnTestBatch.TabIndex = 11;
            this.btnTestBatch.Text = "TEST PERFORMANTA BATCH\r\n(Ruleaza toate abordarile)";
            this.btnTestBatch.UseVisualStyleBackColor = false;
            this.btnTestBatch.Click += new System.EventHandler(this.btnTestBatch_Click);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 20F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(980, 569);
            this.Controls.Add(this.btnTestBatch);
            this.Controls.Add(this.btnDeadlockSolved);
            this.Controls.Add(this.btnDeadlockProblem);
            this.Controls.Add(this.btnLostUpdateSolved);
            this.Controls.Add(this.btnLostUpdateProblem);
            this.Controls.Add(this.btnPhantomSolved);
            this.Controls.Add(this.btnPhantomProblem);
            this.Controls.Add(this.btnNonRepeatableSolved);
            this.Controls.Add(this.btnNonRepeatableProblem);
            this.Controls.Add(this.btnDirtyReadSolved);
            this.Controls.Add(this.btnDirtyReadProblem);
            this.Controls.Add(this.rtbLogs);
            this.Name = "Form1";
            this.Text = "Lab 2: Tranzactii si Niveluri de Izolare";
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.RichTextBox rtbLogs;
        private System.Windows.Forms.Button btnDirtyReadProblem;
        private System.Windows.Forms.Button btnDirtyReadSolved;
        private System.Windows.Forms.Button btnNonRepeatableProblem;
        private System.Windows.Forms.Button btnNonRepeatableSolved;
        private System.Windows.Forms.Button btnPhantomProblem;
        private System.Windows.Forms.Button btnPhantomSolved;
        private System.Windows.Forms.Button btnLostUpdateProblem;
        private System.Windows.Forms.Button btnLostUpdateSolved;
        private System.Windows.Forms.Button btnDeadlockProblem;
        private System.Windows.Forms.Button btnDeadlockSolved;
        private System.Windows.Forms.Button btnTestBatch;
    }
}