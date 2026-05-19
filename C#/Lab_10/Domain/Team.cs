namespace Lab_10.Domain;

public class Team
{
    private String id;
    private String name;

    public Team(string id, string name)
    {
        this.id = id;
        this.name = name;
    }

    public string Id
    {
        get => id; 
        set => id = value;
    }

    public string Name
    {
        get => name;
        set => name = value ?? throw new ArgumentNullException(nameof(value));
    }

    public override string ToString()
    {
        return id + ";" + name;
    }
}