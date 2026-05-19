namespace Lab_10.Repository;

public interface Repository<ID,E>
{
    List<E> findAll();
    E findOne(ID id);
}