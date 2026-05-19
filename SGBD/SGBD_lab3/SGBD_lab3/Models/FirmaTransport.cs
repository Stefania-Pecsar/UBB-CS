using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace SGBD_lab3.Models
{
    [Table("Firma_transport")]
    public class FirmaTransport
    {
        [Key]
        [Column(TypeName = "varchar(100)")]
        public string Caen { get; set; }
        public string Denumire { get; set; }

        [Column("sediu_firma")]
        public string SediuFirma { get; set; }
        public string Telefon { get; set; }
        public string Email { get; set; }

        // virtual activeaza Lazy Loading-ul
        public virtual ICollection<Angajat> Angajati { get; set; } = new List<Angajat>();
    }
}