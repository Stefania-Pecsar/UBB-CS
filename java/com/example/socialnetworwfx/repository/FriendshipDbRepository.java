package com.example.socialnetworwfx.repository;

import com.example.socialnetworwfx.domain.Friendship;
import com.example.socialnetworwfx.domain.validation.Validation;
import com.example.socialnetworwfx.domain.validation.ValidationException;
import com.example.socialnetworwfx.repository.Paginare.Page;
import com.example.socialnetworwfx.repository.Paginare.Pageable;

import java.sql.*;
import java.util.*;

public class FriendshipDbRepository extends AbstractDbRepository<Long, Friendship> {
    public FriendshipDbRepository(String url, String username, String password, Validation<Friendship> validator) {
        super(url, username, password, validator);
    }

    @Override
    public Optional<Friendship> findOne(Long id) {
        try (Connection connection = DriverManager.getConnection(getUrl(), getUsername(), getPassword());) {
            PreparedStatement statement = connection.prepareStatement("SELECT * FROM prieteni WHERE id = ?");
            statement.setLong(1, id);
            ResultSet resultSet = statement.executeQuery();
            if (resultSet.next()) {
                Long ID = resultSet.getLong("id");
                Long ID1 = resultSet.getLong("id1");
                Long ID2 = resultSet.getLong("id2");
                Friendship friendship = new Friendship(ID1, ID2);
                friendship.setID(ID);
                return Optional.of(friendship);
            }

        } catch (SQLException e) {
            e.printStackTrace();
        }
        return Optional.empty();
    }

    @Override
    public Page<Friendship> findAllOnPage(Pageable pageable) {
        List<Friendship> friendships = new ArrayList<>();
        int totalCount = 0;

        try (Connection connection = DriverManager.getConnection(getUrl(), getUsername(), getPassword())) {
            // pt numărul total de elemente
            String countQuery = "SELECT COUNT(*) AS count FROM prieteni";
            try (PreparedStatement countStatement = connection.prepareStatement(countQuery);
                 ResultSet countResultSet = countStatement.executeQuery()) {
                if (countResultSet.next()) {
                    totalCount = countResultSet.getInt("count");
                }
            }

            // pt obț prieteni paginați
            String pageQuery = "SELECT * FROM prieteni LIMIT ? OFFSET ?";
            try (PreparedStatement pageStatement = connection.prepareStatement(pageQuery)) {
                pageStatement.setInt(1, pageable.getPageSize()); // Setăm dimensiunea paginii
                pageStatement.setInt(2, pageable.getPageNr() * pageable.getPageSize()); // Calculăm offset-ul

                try (ResultSet pageResultSet = pageStatement.executeQuery()) {
                    while (pageResultSet.next()) {
                        Long ID = pageResultSet.getLong("id");
                        Long ID1 = pageResultSet.getLong("id1");
                        Long ID2 = pageResultSet.getLong("id2");

                        Friendship friendship = new Friendship(ID1, ID2);
                        friendship.setID(ID);
                        friendships.add(friendship);
                    }
                }
            }

        } catch (SQLException e) {
           throw new RuntimeException(e);
        }

        return new Page<>(totalCount, friendships);
    }

    public long getTotalCount(Long userId) {
        String countQuery = "SELECT COUNT(*) FROM prieteni WHERE id1 = ? OR id2 = ?";
        try (Connection connection = DriverManager.getConnection(getUrl(), getUsername(), getPassword());
             PreparedStatement statement = connection.prepareStatement(countQuery)) {

            statement.setLong(1, userId);
            statement.setLong(2, userId);
            ResultSet resultSet = statement.executeQuery();

            if (resultSet.next()) {
                return resultSet.getLong(1);
            }
        } catch (SQLException e) {
            throw new RuntimeException( e.getMessage(), e);
        }
        return 0;
    }

    @Override
    public Iterable<Friendship> findAll() {
        Set<Friendship> friendships = new HashSet<>();
        try (Connection connection = DriverManager.getConnection(getUrl(), getUsername(), getPassword())) {
            PreparedStatement statement = connection.prepareStatement("SELECT * FROM prieteni");
            ResultSet resultSet = statement.executeQuery();
            while (resultSet.next()) {
                Long ID = resultSet.getLong("id");
                Long ID1 = resultSet.getLong("id1");
                Long ID2 = resultSet.getLong("id2");
                Friendship friendship = new Friendship(ID1, ID2);
                friendship.setID(ID);
                friendships.add(friendship);
            }
            return friendships;
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return friendships;
    }

    @Override
    public Optional<Friendship> save(Friendship entity) {
        int rez = -1;
        try (Connection connection = DriverManager.getConnection(getUrl(), getUsername(), getPassword());
             PreparedStatement statement = connection.prepareStatement("INSERT INTO prieteni (id1,id2,friendsfrom) VALUES (?,?,?)");
        ) {
            getValidator().validate(entity);
            statement.setLong(1, entity.getFirstFriend());
            statement.setLong(2, entity.getSecondFriend());
            statement.setTimestamp(3, Timestamp.valueOf(entity.getFriendsFrom()));
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
    public Optional<Friendship> delete(Long id) {
        try (Connection connection = DriverManager.getConnection(getUrl(), getUsername(), getPassword())) {
            Optional<Friendship> friendship = findOne(id);
            if (friendship.isEmpty()) {
                return Optional.empty();
            }
            PreparedStatement statement = connection.prepareStatement("DELETE FROM prieteni WHERE id = ?");
            statement.setLong(1, id);
            int rowsAffected = statement.executeUpdate();

            if (rowsAffected > 0) {
                return friendship;
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return Optional.empty();
    }

    @Override
    public Optional<Friendship> update(Friendship entity) {
        try (Connection connection = DriverManager.getConnection(getUrl(), getUsername(), getPassword())) {
            Optional<Friendship> friendship = findOne(entity.getID());
            if (friendship.isEmpty()) {
                return Optional.of(entity);
            }
            getValidator().validate(entity);
            PreparedStatement statement = connection.prepareStatement("UPDATE prieteni SET id1=?,id2=?WHERE id = ? ");
            statement.setLong(1, entity.getFirstFriend());
            statement.setLong(2, entity.getSecondFriend());
            statement.setLong(3, entity.getID());
            int rowsAffected = statement.executeUpdate();
            if (rowsAffected > 0) {
                return Optional.of(entity);
            }
        } catch (SQLException | ValidationException e) {
            e.getMessage();
        }
        return Optional.empty();
    }



}

