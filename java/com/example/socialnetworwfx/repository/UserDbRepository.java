package com.example.socialnetworwfx.repository;

import com.example.socialnetworwfx.domain.User;
import com.example.socialnetworwfx.domain.validation.Validation;
import com.example.socialnetworwfx.domain.validation.ValidationException;
import com.example.socialnetworwfx.repository.Paginare.Page;
import com.example.socialnetworwfx.repository.Paginare.Pageable;
import com.example.socialnetworwfx.repository.Paginare.PagingRepository;

import java.sql.*;
import java.util.*;



public class UserDbRepository extends AbstractDbRepository<Long, User> {
    public UserDbRepository(String url, String username, String password, Validation<User> validator) {
        super(url,username,password,validator);
    }

    @Override
    public Optional<User> findOne(Long id) {
        try (Connection connection = DriverManager.getConnection(getUrl(), getUsername(), getPassword());) {
            PreparedStatement statement = connection.prepareStatement("SELECT * FROM UTILIZATORI WHERE \"id\" = ?");
            statement.setLong(1, id);
            ResultSet resultSet = statement.executeQuery();
            if (resultSet.next()) {
                Long ID1 = resultSet.getLong("id");
                String firstName1 = resultSet.getString("first_name");
                String lastName1 = resultSet.getString("last_name");
                String email1 = resultSet.getString("email");
                String password1 = resultSet.getString("password");
                User user1 = new User(firstName1, lastName1, email1, password1);
                user1.setID(ID1);
                return Optional.of(user1);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return Optional.empty();
    }
    @Override
    public Iterable<User> findAll() {
        Set<User> users = new HashSet<>();
        try (Connection connection = DriverManager.getConnection(getUrl(), getUsername(), getPassword());
             PreparedStatement statement = connection.prepareStatement("SELECT * from \"utilizatori\"");
             ResultSet resultSet = statement.executeQuery()){
            while (resultSet.next()) {
                Long ID1 = resultSet.getLong("id");
                String firstName1 = resultSet.getString("first_name");
                String lastName1 = resultSet.getString("last_name");
                String email = resultSet.getString("email");
                String password = resultSet.getString("password");
                User user1 = new User(firstName1, lastName1, email, password);
                user1.setID(ID1);
                users.add(user1);
            }
            return users;
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return users;
    }
    @Override
    public Optional<User> save(User entity) {
        int rez = -1;
        try (Connection connection = DriverManager.getConnection(getUrl(), getUsername(), getPassword());
             PreparedStatement statement = connection.prepareStatement("INSERT INTO utilizatori (\"first_name\", \"last_name\",\"email\",\"password\") VALUES (?, ?, ?, ?)")){
            statement.setString(1, entity.getFirstName());
            statement.setString(2, entity.getLastName());
            statement.setString(3, entity.getEmail());
            statement.setString(4, entity.getPassword());
            rez = statement.executeUpdate();
        } catch (SQLException | ValidationException e) {
            e.getMessage();
        }
        if (rez > 0)
            return Optional.empty();
        else
            return Optional.of(entity);
    }

    @Override
    public Optional<User> delete(Long id) {
        try (Connection connection = DriverManager.getConnection(getUrl(), getUsername(), getPassword());) {
            Optional<User> user = findOne(id);
            if (user.isEmpty()) {
                return Optional.empty();
            }
            PreparedStatement statement = connection.prepareStatement("DELETE FROM utilizatori WHERE id = ?");
            statement.setLong(1, id);
            int rowsAffected = statement.executeUpdate();

            if (rowsAffected > 0) {
                return user;
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return Optional.empty();
    }
    @Override
    public Optional<User> update(User entity) {
        try (Connection connection = DriverManager.getConnection(getUrl(), getUsername(),getPassword());) {
            Optional<User> user = findOne(entity.getID());
            if (user.isEmpty()) {
                return Optional.of(entity);
            }
            getValidator().validate(entity);
            PreparedStatement statement = connection.prepareStatement("UPDATE utilizatori SET first_name=?, last_name=?,email=?,password=? WHERE id = ?");
            statement.setString(1, entity.getFirstName());
            statement.setString(2, entity.getLastName());
            statement.setString(3, entity.getEmail());
            statement.setString(4, entity.getPassword());
            statement.setLong(5, entity.getID());
            int rowsAffected = statement.executeUpdate();
            if (rowsAffected > 0) {
                return Optional.of(entity);
            }
        } catch (SQLException | ValidationException e) {
            e.getMessage();
        }
        return Optional.empty();
    }

    @Override
    public Page<User> findAllOnPage(Pageable pageable) {
        List<User> users = new ArrayList<>();
        try (Connection connection = DriverManager.getConnection(getUrl(), getUsername(), getPassword())) {
           PreparedStatement pageStatement = connection.prepareStatement(
                    "SELECT * FROM utilizatori LIMIT ? OFFSET ?"
            );
            PreparedStatement countStatement = connection.prepareStatement(
                    "SELECT COUNT(*) AS count FROM utilizatori"
            );

            pageStatement.setInt(1, pageable.getPageSize());
            pageStatement.setInt(2, pageable.getPageSize() * pageable.getPageNr());

            try (ResultSet pageResultSet = pageStatement.executeQuery();
                 ResultSet countResultSet = countStatement.executeQuery()) {

                int count = 0;
                if (countResultSet.next()) {
                    count = countResultSet.getInt("count");
                }

                while (pageResultSet.next()) {
                    Long ID = pageResultSet.getLong("id");
                    String firstName = pageResultSet.getString("first_name");
                    String lastName = pageResultSet.getString("last_name");
                    String email = pageResultSet.getString("email");
                    String password = pageResultSet.getString("password");

                    User user = new User(firstName, lastName, email, password);
                    user.setID(ID);
                    users.add(user);
                }

                return new Page<>(count, users);
            }

        } catch (SQLException e) {
            e.printStackTrace();
        }

        return new Page<>(0, new ArrayList<>());
    }
}