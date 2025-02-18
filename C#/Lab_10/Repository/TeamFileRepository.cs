using System.Runtime.InteropServices.JavaScript;
using Lab_10.Domain;

namespace Lab_10.Repository;

public class TeamFileRepository : Repository<String,Team>
{
    private String fileNamel;
    private List<Team> teams;

    public TeamFileRepository(string fileName)
    {
        fileNamel = fileName;
        teams = new List<Team>();
        loadData();
    }

    private void loadData()
    {
        String[] lines = File.ReadAllLines(fileNamel);

        foreach (string line in lines )
        {
            String[] attributes = line.Split(";",2,StringSplitOptions.RemoveEmptyEntries);
            Team team = new Team(attributes[0], attributes[1]);
            teams.Add(team);
        }
    }

    public Team findOne(String id)
    {
        foreach (Team team in teams)
        {
            if (team.Id == id)
            {
                return team;
            }
        }
        return null;
    }

    public List<Team> findAll()
    {
        return teams;
    }
}