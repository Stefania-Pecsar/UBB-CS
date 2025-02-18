namespace Lab_10.Domain;

public class Match
{
    private String id;
    private Team team1;
    private Team team2;
    private DateTime date;

    public Match(string id, Team team1, Team team2, DateTime date)
    {
        this.id = id;
        this.team1 = team1;
        this.team2 = team2;
        this.date = date;
    }

    public string Id
    {
        get => id;
        set => id = value ?? throw new ArgumentNullException(nameof(value));
    }

    public Team Team1
    {
        get => team1;
        set => team1 = value ?? throw new ArgumentNullException(nameof(value));
    }

    public Team Team2
    {
        get => team2;
        set => team2 = value ?? throw new ArgumentNullException(nameof(value));
    }

    public DateTime Date
    {
        get => date;
        set => date = value;
    }

    public override string ToString()
    {
        return team1 + ";" + team2+ ";"+date;
    }
}