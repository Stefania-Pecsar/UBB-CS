using System.ComponentModel;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace SGBD_lab3.Models
{
    [Table("Angajati")]
    public class Angajat
    {
        [Key]
        [Column(TypeName = "varchar(100)")]
        public string Cnp { get; set; }

        [ForeignKey("FirmaTransport")]
        [Column(TypeName = "varchar(100)")]
        public string Caen { get; set; }

        public string Nume { get; set; }
        public string Prenume { get; set; }
        public string Functie { get; set; }
        public decimal Salar { get; set; }
        public double Bonusuri { get; set; }

        //news
        public string TelefonAngajat { get; set; }

        [Timestamp]
        public byte[] RowVersion { get; set; }
        public bool IsDeleted { get; set; } = false;
        public DateTime? DeletedAt { get; set; }
        public string DeletedBy { get; set; }

        [Browsable(false)]
        public virtual FirmaTransport FirmaTransport { get; set; }
    }
}
