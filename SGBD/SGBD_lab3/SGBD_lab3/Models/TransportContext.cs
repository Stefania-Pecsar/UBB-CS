using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using System.IO;

namespace SGBD_lab3.Models
{
    public class TransportContext : DbContext
    {
        public DbSet<FirmaTransport> FirmeTransport { get; set; }
        public DbSet<Angajat> Angajati { get; set; }
        public DbSet<Proiect> Proiect { get; set; }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            if (!optionsBuilder.IsConfigured)
            {
                var builder = new ConfigurationBuilder()
                    .SetBasePath(Directory.GetCurrentDirectory())
                    .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true);

                string connectionString = builder.Build().GetConnectionString("DefaultConnection");

                optionsBuilder.UseLazyLoadingProxies()
                               .UseSqlServer(connectionString)
                               .LogTo(Console.WriteLine, LogLevel.Information)
                               .EnableSensitiveDataLogging();
            }
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            modelBuilder.Entity<Angajat>()
                .HasIndex(a => a.Salar)
                .HasDatabaseName("idx_angajati_salar");

            modelBuilder.Entity<Angajat>()
                .HasIndex(a => a.Caen)
                .HasDatabaseName("idx_angajati_caen");


            modelBuilder.Entity<Angajat>()
                .HasIndex(a => new { a.Caen, a.Salar })
                .HasDatabaseName("idx_angajati_caen_salar");

            modelBuilder.Entity<Angajat>().HasQueryFilter(a => !a.IsDeleted);
        }

    }
}