package com.example.socialnetworwfx.repository;

import com.example.socialnetworwfx.domain.Message;
import com.example.socialnetworwfx.domain.User;
import com.example.socialnetworwfx.domain.validation.Validation;
import com.example.socialnetworwfx.repository.Paginare.Page;
import com.example.socialnetworwfx.repository.Paginare.Pageable;

import java.sql.*;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Optional;

public class MessageDbRepository extends AbstractDbRepository<Long, Message> {
    private final UserDbRepository userDbRepository; // Instanță pentru UserDbRepository

    public MessageDbRepository(String url, String username, String password, Validation<Message> validator, UserDbRepository userDbRepository) {
        super(url, username, password, validator);
        this.userDbRepository = userDbRepository;
    }

    @Override
    public Optional<Message> save(Message entity) {
        if (getValidator() != null) {
            getValidator().validate(entity);
        }
        String query = "INSERT INTO mesaje(from_id, to_id, date, message, reply_id) VALUES (?,?,?,?,?)";
        try (Connection connection = DriverManager.getConnection(getUrl(), getUsername(), getPassword());
             PreparedStatement statement = connection.prepareStatement(query, Statement.RETURN_GENERATED_KEYS)) {

            statement.setLong(1, entity.getFrom().getID());
            statement.setLong(2, entity.getTo().get(0).getID());
            statement.setTimestamp(3, Timestamp.valueOf(entity.getData()));
            statement.setString(4, entity.getMessage());
            if (entity.getReply() == null) {
                statement.setNull(5, Types.NULL);
            } else {
                statement.setLong(5, entity.getReply().getId());
            }
            int rowsAffected = statement.executeUpdate();

            if (rowsAffected > 0) {
                ResultSet generatedKeys = statement.getGeneratedKeys();
                if (generatedKeys.next()) {
                    entity.setId(generatedKeys.getLong(1));
                }
                return Optional.of(entity);
            }
        } catch (SQLException e) {
            throw new RuntimeException("Database error during save operation: " + e.getMessage(), e);
        }

        return Optional.empty();
    }

    @Override
    public Optional<Message> delete(Long id) {
        // Conectare la baza de date și obținerea detaliilor mesajului
        try (Connection connection = DriverManager.getConnection(getUrl(), getUsername(), getPassword())) {
            // Căutăm mesajul pe baza ID-ului
            Optional<Message> message = findOne(id);
            if (message.isEmpty()) {
                // Dacă mesajul nu există, returnăm Optional.empty()
                return Optional.empty();
            }

            // Dacă mesajul există, îl ștergem
            String query = "DELETE FROM mesaje WHERE id = ?";
            try (PreparedStatement statement = connection.prepareStatement(query)) {
                statement.setLong(1, id); // Setăm ID-ul mesajului în interogare
                int rowsAffected = statement.executeUpdate(); // Executăm interogarea de ștergere

                // Dacă mesajul a fost șters, returnăm obiectul mesaj șters
                if (rowsAffected > 0) {
                    return message;
                }
            }
        } catch (SQLException e) {
            e.printStackTrace(); // Poți trata excepția mai elegant, în funcție de cerințele tale
        }

        // Dacă nu s-a șters niciun mesaj, returnăm Optional.empty()
        return Optional.empty();
    }

    @Override
    public Optional<Message> update(Message entity) {
        // Validăm mesajul înainte de a-l salva în baza de date (opțional, în funcție de validatorul specificat)
        if (getValidator() != null) {
            getValidator().validate(entity);
        }

        // Definim interogarea SQL pentru actualizarea unui mesaj
        String query = "UPDATE mesaje SET from_id = ?, to_id = ?, date = ?, message = ?, reply_id = ? WHERE id = ?";

        try (Connection connection = DriverManager.getConnection(getUrl(), getUsername(), getPassword());
             PreparedStatement statement = connection.prepareStatement(query)) {

            // Setăm valorile pentru interogare
            statement.setLong(1, entity.getFrom().getID());  // Setăm ID-ul utilizatorului care a trimis mesajul
            statement.setLong(2, entity.getTo().get(0).getID());  // Setăm ID-ul utilizatorului care a primit mesajul
            statement.setTimestamp(3, Timestamp.valueOf(entity.getData()));  // Setăm data mesajului
            statement.setString(4, entity.getMessage());  // Setăm conținutul mesajului

            // Setăm reply_id (dacă există)
            if (entity.getReply() == null) {
                statement.setNull(5, Types.NULL);  // Dacă nu există un mesaj de răspuns, setăm NULL
            } else {
                statement.setLong(5, entity.getReply().getId());  // Setăm ID-ul mesajului de răspuns
            }

            statement.setLong(6, entity.getId());  // Setăm ID-ul mesajului care trebuie actualizat

            // Executăm actualizarea în baza de date
            int rowsAffected = statement.executeUpdate();

            // Dacă actualizarea a avut succes, returnăm mesajul actualizat
            if (rowsAffected > 0) {
                return Optional.of(entity);
            }

        } catch (SQLException e) {
            e.printStackTrace();  // Tratarea excepției de SQL
        }

        // Dacă actualizarea nu a avut loc, returnăm Optional.empty()
        return Optional.empty();
    }

    public Optional<Message> findOneNoReply(Long id) {
        String query = "SELECT * FROM mesaje WHERE id = ?";
        try (Connection connection = DriverManager.getConnection(getUrl(), getUsername(), getPassword());
             PreparedStatement statement = connection.prepareStatement(query)) {

            statement.setLong(1, id);
            ResultSet resultSet = statement.executeQuery();

            if (resultSet.next()) {
                Long fromId = resultSet.getLong("from_id");
                Long toId = resultSet.getLong("to_id");
                String message = resultSet.getString("message");
                LocalDateTime date = resultSet.getTimestamp("date").toLocalDateTime();

                // Obține utilizatorii folosind instanța UserDbRepository
                Optional<User> fromUser = userDbRepository.findOne(fromId);
                Optional<User> toUser = userDbRepository.findOne(toId);

                if (fromUser.isEmpty() || toUser.isEmpty()) {
                    return Optional.empty(); // Nu a găsit utilizatorii
                }

                Message msg = new Message(fromUser.get(), Collections.singletonList(toUser.get()), message, date);
                msg.setId(id);
                return Optional.of(msg);
            }

        } catch (SQLException e) {
            throw new RuntimeException("Database operation failed: " + e.getMessage(), e);
        }
        return Optional.empty();
    }

    @Override
    public Optional<Message> findOne(Long id) {
        Optional<Message> msgOptional = findOneNoReply(id);
        if (msgOptional.isEmpty()) {
            return Optional.empty();
        }
        Message msg = msgOptional.get();

        String query = "SELECT reply_id FROM mesaje WHERE id = ?";
        try (Connection connection = DriverManager.getConnection(getUrl(), getUsername(), getPassword());
             PreparedStatement statement = connection.prepareStatement(query)) {

            statement.setLong(1, id);
            ResultSet resultSet = statement.executeQuery();

            if (resultSet.next()) {
                Long replyId = resultSet.getLong("reply_id");
                if (replyId != 0) {
                    Optional<Message> replyMessageOptional = findOneNoReply(replyId);
                    replyMessageOptional.ifPresent(msg::setReply);
                }
            }

        } catch (SQLException e) {
            throw new RuntimeException("Failed to fetch reply for message: " + e.getMessage(), e);
        }

        return Optional.of(msg);
    }

    @Override
    public Iterable<Message> findAll() {
        List<Message> messages = new ArrayList<>();
        String query = "SELECT * FROM mesaje";
        try (Connection connection = DriverManager.getConnection(getUrl(), getUsername(), getPassword());
             PreparedStatement statement = connection.prepareStatement(query)) {

            ResultSet resultSet = statement.executeQuery();
            while (resultSet.next()) {
                Long id = resultSet.getLong("id");
                Long fromId = resultSet.getLong("from_id");
                Long toId = resultSet.getLong("to_id");
                LocalDateTime date = resultSet.getTimestamp("date").toLocalDateTime();
                String message = resultSet.getString("message");
                Long replyId = resultSet.getLong("reply_id");

                Optional<User> fromUser = userDbRepository.findOne(fromId);
                Optional<User> toUser = userDbRepository.findOne(toId);

                if (fromUser.isPresent() && toUser.isPresent()) {
                    Message msg = new Message(fromUser.get(), Collections.singletonList(toUser.get()), message, date);
                    msg.setId(id);
                    if (replyId != 0) {
                        Optional<Message> replyMessageOptional = findOneNoReply(replyId);
                        replyMessageOptional.ifPresent(msg::setReply);
                    }
                    messages.add(msg);
                }
            }

        } catch (SQLException e) {
            throw new RuntimeException("Failed to fetch messages: " + e.getMessage(), e);
        }
        return messages;
    }

    @Override
    public Page<Message> findAllOnPage(Pageable pageable) {
        List<Message> messages = new ArrayList<>();
        String query = "SELECT * FROM mesaje ORDER BY date LIMIT ? OFFSET ?";

        try (Connection connection = DriverManager.getConnection(getUrl(), getUsername(), getPassword());
             PreparedStatement statement = connection.prepareStatement(query)) {

            statement.setInt(1, pageable.getPageSize());
            statement.setInt(2, pageable.getPageNr() * pageable.getPageSize()); // Calculate offset

            ResultSet resultSet = statement.executeQuery();

            while (resultSet.next()) {
                Long id = resultSet.getLong("id");
                Long fromId = resultSet.getLong("from_id");
                Long toId = resultSet.getLong("to_id");
                LocalDateTime date = resultSet.getTimestamp("date").toLocalDateTime();
                String message = resultSet.getString("message");
                Long replyId = resultSet.getLong("reply_id");

                Optional<User> fromUser = userDbRepository.findOne(fromId);
                Optional<User> toUser = userDbRepository.findOne(toId);

                if (fromUser.isPresent() && toUser.isPresent()) {
                    Message msg = new Message(fromUser.get(), Collections.singletonList(toUser.get()), message, date);
                    msg.setId(id);
                    if (replyId != 0) {
                        Optional<Message> replyMessageOptional = findOneNoReply(replyId);
                        replyMessageOptional.ifPresent(msg::setReply);
                    }
                    messages.add(msg);
                }
            }
        } catch (SQLException e) {
            throw new RuntimeException( e.getMessage(), e);
        }
        return new Page<>(0, new ArrayList<>());
    }
}
