using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace SGBD_lab3.Models
{
    [Table("Proiecte")]
    public class Proiect 
    {
        [Key] 
        public int Id { get; set; }

        [Required]
        [MaxLength(100)] 
        public string Nume { get; set; }

        public string Descriere { get; set; } 

        public DateTime DataStart { get; set; } 


        [ForeignKey("FirmaTransport")]

        [Column(TypeName = "varchar(100)")]
        public string CaenFirma { get; set; }

        public virtual FirmaTransport FirmaTransport { get; set; }
    }
}