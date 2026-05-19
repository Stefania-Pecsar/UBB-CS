namespace Lab_10.Domain;

public class ActivePlayer
{
    private string id;
    private string idPlayer;
    private string idMatch;
    private int nrPointsScored;
    private String tip;

    public ActivePlayer(string id, string idPlayer, string idMatch, int nrPointsScored, string tip)
    {
        this.id = id;
        this.idPlayer = idPlayer;
        this.idMatch = idMatch;
        this.nrPointsScored = nrPointsScored;
        this.tip = tip;
    }

    public string Id
    {
        get => id;
        set => id = value ?? throw new ArgumentNullException(nameof(value));
    }

    public string IdPlayer
    {
        get => idPlayer;
        set => idPlayer = value ?? throw new ArgumentNullException(nameof(value));
    }

    public string IdMatch
    {
        get => idMatch;
        set => idMatch = value ?? throw new ArgumentNullException(nameof(value));
    }

    public int NrPointsScored
    {
        get => nrPointsScored;
        set => nrPointsScored = value;
    }

    public string Tip
    {
        get => tip;
        set => tip = value ?? throw new ArgumentNullException(nameof(value));
    }

    public override string ToString()
    {
        return idPlayer + ";" + idMatch + ";" + nrPointsScored + ";" + tip;
    }
}