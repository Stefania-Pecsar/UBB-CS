using System.Globalization;
using Lab_10.Domain;

namespace Lab_10.Repository;

public class MatchFileRepository : Repository<String, Match>
{
    private String _fileName;
    private List<Match> _matches;

    public MatchFileRepository(string fileName)
    {
        _fileName = fileName;
        _matches = new List<Match>();
        loadData();
    }

    private void loadData()
    {
        String[] lines = File.ReadAllLines(_fileName);
        
        foreach (string line in lines)
        {
            String[] attr = line.Split(";", 4, StringSplitOptions.RemoveEmptyEntries);
            String team1_id = attr[1];
            String team2_id = attr[2];
            TeamFileRepository teamFileRepository =
                new TeamFileRepository(
                    "C:\\Users\\FANE\\Desktop\\fac\\AN 2\\MAP\\Lab_10\\Lab_10\\files\\teams.txt");
            Team team1 = teamFileRepository.findOne(team1_id);
            Team team2 = teamFileRepository.findOne(team2_id);

            Match match = new Match(attr[0], team1, team2, DateTime.ParseExact(attr[3], "dd/MM/yyyy HH:mm", CultureInfo.InvariantCulture));
            _matches.Add(match);
        }
    }
    
    public Match findOne(string id)
    {
        foreach (Match meci in _matches)
        {
            if (meci.Id == id)
            {
                return meci;
            }
        }

        return null;
    }

    public List<Match> findAll()
    {
        return _matches;
    }
    
}