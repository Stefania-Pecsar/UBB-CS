namespace Lab_10.Domain;

public class Player : Student
{
    private Team _team;

    public Player(string name, string id, string school) : base(name, id, school)
    {
    }

    public Player(string name, string id, string school, Team team) : base(name, id, school)
    {
        _team = team;
    }

    public Team Team
    {
        get => _team;
        set => _team = value ?? throw new ArgumentNullException(nameof(value));
    }

    public override string ToString()
    {
        return base.ToString() + ";" + _team;
    }
}