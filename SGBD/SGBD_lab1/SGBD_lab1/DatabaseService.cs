<<<<<<< Updated upstream
﻿using Microsoft.Data.SqlClient;
using System.Collections.Generic; 
using System.Data;

namespace SGBD_lab1
{
    public class DatabaseService
    {

        public string ConnectionString = "Server=DESKTOP-I0292P0\\SQLEXPRESS;Database=FirmaDeTransportExtern;Integrated Security=True;TrustServerCertificate=true";

        public void ExecuteNonQuery(string query, List<SqlParameter> parameters)
        {
            using (SqlConnection connection = new SqlConnection(ConnectionString))
            {
                SqlCommand command = new SqlCommand(query, connection);
                command.Parameters.AddRange(parameters.ToArray());
                connection.Open();
                command.ExecuteNonQuery();
            }
        }
    }
=======
﻿using Microsoft.Data.SqlClient;
using System.Collections.Generic; 
using System.Data;

namespace SGBD_lab1
{
    public class DatabaseService
    {

        public string ConnectionString = "Server=DESKTOP-I0292P0\\SQLEXPRESS;Database=FirmaDeTransportExtern;Integrated Security=True;TrustServerCertificate=true";

        public void ExecuteNonQuery(string query, List<SqlParameter> parameters)
        {
            using (SqlConnection connection = new SqlConnection(ConnectionString))
            {
                SqlCommand command = new SqlCommand(query, connection);
                command.Parameters.AddRange(parameters.ToArray());
                connection.Open();
                command.ExecuteNonQuery();
            }
        }
    }
>>>>>>> Stashed changes
}