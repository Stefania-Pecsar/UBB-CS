namespace Lab_10.Domain;

public class Student
{
    private string name;
    private String id;
    private String school;

    public Student(string name, string id, string school)
    {
        this.name = name;
        this.id = id;
        this.school = school;
    }
    
    public string Name 
    { 
        get => name;
        set => name = value; 
    }

    public string Id
    {
        get => id;
        set => id = value ?? throw new ArgumentNullException(nameof(value));
    }

    public string School
    {
        get => school;
        set => school = value ?? throw new ArgumentNullException(nameof(value));
    }

    public override string ToString()
    {
        return id + ";" + name + ";" + school;
    }
}