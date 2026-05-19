using Microsoft.EntityFrameworkCore;
using SGBD_lab3.Models;
using System;
using System.Windows.Forms;

namespace SGBD_lab3
{
    internal static class Program
    {
        /// <summary>
        ///  The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            // To customize application configuration such as set high DPI settings or default font,
            // see https://aka.ms/applicationconfiguration.
            using (var context = new TransportContext())
            {
                context.Database.EnsureCreated();
                Console.WriteLine("Database schema verified/created.");
            }
            ApplicationConfiguration.Initialize();
            Application.Run(new Form1());
        }
    }
}