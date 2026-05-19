using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace SGBD_lab3.Migrations
{
    public partial class SeedProiecte : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.Sql(@"
                IF NOT EXISTS (SELECT 1 FROM Proiecte WHERE Nume = 'Proiect A')
                BEGIN
                    INSERT INTO Proiecte (Nume, Descriere, DataStart, CaenFirma)
                    VALUES 
                        ('Sistem flotă', 'Management flotă auto', '2025-01-15', '4941'),
                        ('Aplicație livrări', 'Urmărire comenzi în timp real', '2025-02-01', '5221'),
                        ('Optimizare rute', 'Algoritm de rute eficiente', '2025-03-10', '5229');
                END
            ");
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.Sql("DELETE FROM Proiecte WHERE Nume IN ('Sistem flotă', 'Aplicație livrări', 'Optimizare rute')");
        }
    }
}