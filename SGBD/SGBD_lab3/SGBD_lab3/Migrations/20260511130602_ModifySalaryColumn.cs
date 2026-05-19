using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace SGBD_lab3.Migrations
{
    public partial class ModifySalaryColumn : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            // 1. Șterge indexurile care depind de coloana Salar
            migrationBuilder.DropIndex(
                name: "idx_angajati_salar",
                table: "Angajati");

            migrationBuilder.DropIndex(
                name: "idx_angajati_caen_salar",
                table: "Angajati");

            // 2. Verificare siguranță date (opțional, dar păstreaz-o)
            migrationBuilder.Sql(@"
                IF EXISTS (SELECT 1 FROM Angajati WHERE Salar > 9999999999.99 OR Salar < -9999999999.99)
                BEGIN
                    RAISERROR('Exista salarii care depasesc domeniul decimal(12,2)', 16, 1);
                END
            ");

            // 3. Modifică tipul coloanei (corect, cu actualizarea snapshot-ului)
            migrationBuilder.AlterColumn<decimal>(
                name: "Salar",
                table: "Angajati",
                type: "decimal(12,2)",
                nullable: false,
                oldClrType: typeof(double),
                oldType: "float");

            // 4. Recrează indexurile
            migrationBuilder.CreateIndex(
                name: "idx_angajati_salar",
                table: "Angajati",
                column: "Salar");

            migrationBuilder.CreateIndex(
                name: "idx_angajati_caen_salar",
                table: "Angajati",
                columns: new[] { "Caen", "Salar" });
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            // Șterge indexurile
            migrationBuilder.DropIndex(
                name: "idx_angajati_salar",
                table: "Angajati");

            migrationBuilder.DropIndex(
                name: "idx_angajati_caen_salar",
                table: "Angajati");

            // Revenire la tipul float (tot cu AlterColumn, pentru coerență)
            migrationBuilder.AlterColumn<double>(
                name: "Salar",
                table: "Angajati",
                type: "float",
                nullable: false,
                oldClrType: typeof(decimal),
                oldType: "decimal(12,2)");

            // Recrează indexurile
            migrationBuilder.CreateIndex(
                name: "idx_angajati_salar",
                table: "Angajati",
                column: "Salar");

            migrationBuilder.CreateIndex(
                name: "idx_angajati_caen_salar",
                table: "Angajati",
                columns: new[] { "Caen", "Salar" });
        }
    }
}