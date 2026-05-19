using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace SGBD_lab3.Migrations
{
    /// <inheritdoc />
    public partial class Lab5_FunctionalitatiNoi : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AlterColumn<string>(
                name: "Caen",
                table: "Firma_transport",
                type: "varchar(100)",
                nullable: false,
                oldClrType: typeof(string),
                oldType: "nvarchar(450)");

            migrationBuilder.AlterColumn<string>(
                name: "Caen",
                table: "Angajati",
                type: "varchar(100)",
                nullable: false,
                oldClrType: typeof(string),
                oldType: "nvarchar(450)");

            migrationBuilder.AlterColumn<string>(
                name: "Cnp",
                table: "Angajati",
                type: "varchar(100)",
                nullable: false,
                oldClrType: typeof(string),
                oldType: "nvarchar(450)");

            migrationBuilder.AddColumn<DateTime>(
                name: "DeletedAt",
                table: "Angajati",
                type: "datetime2",
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "DeletedBy",
                table: "Angajati",
                type: "nvarchar(max)",
                nullable: false,
                defaultValue: "");

            migrationBuilder.AddColumn<bool>(
                name: "IsDeleted",
                table: "Angajati",
                type: "bit",
                nullable: false,
                defaultValue: false);

            migrationBuilder.AddColumn<byte[]>(
                name: "RowVersion",
                table: "Angajati",
                type: "rowversion",
                rowVersion: true,
                nullable: false,
                defaultValue: new byte[0]);

            migrationBuilder.AddColumn<string>(
                name: "TelefonAngajat",
                table: "Angajati",
                type: "nvarchar(max)",
                nullable: false,
                defaultValue: "");

            migrationBuilder.CreateTable(
                name: "Proiecte",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Nume = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: false),
                    Descriere = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    DataStart = table.Column<DateTime>(type: "datetime2", nullable: false),
                    CaenFirma = table.Column<string>(type: "varchar(100)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Proiecte", x => x.Id);
                    table.ForeignKey(
                        name: "FK_Proiecte_Firma_transport_CaenFirma",
                        column: x => x.CaenFirma,
                        principalTable: "Firma_transport",
                        principalColumn: "Caen",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_Proiecte_CaenFirma",
                table: "Proiecte",
                column: "CaenFirma");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "Proiecte");

            migrationBuilder.DropColumn(
                name: "DeletedAt",
                table: "Angajati");

            migrationBuilder.DropColumn(
                name: "DeletedBy",
                table: "Angajati");

            migrationBuilder.DropColumn(
                name: "IsDeleted",
                table: "Angajati");

            migrationBuilder.DropColumn(
                name: "RowVersion",
                table: "Angajati");

            migrationBuilder.DropColumn(
                name: "TelefonAngajat",
                table: "Angajati");

            migrationBuilder.AlterColumn<string>(
                name: "Caen",
                table: "Firma_transport",
                type: "nvarchar(450)",
                nullable: false,
                oldClrType: typeof(string),
                oldType: "varchar(100)");

            migrationBuilder.AlterColumn<string>(
                name: "Caen",
                table: "Angajati",
                type: "nvarchar(450)",
                nullable: false,
                oldClrType: typeof(string),
                oldType: "varchar(100)");

            migrationBuilder.AlterColumn<string>(
                name: "Cnp",
                table: "Angajati",
                type: "nvarchar(450)",
                nullable: false,
                oldClrType: typeof(string),
                oldType: "varchar(100)");
        }
    }
}
