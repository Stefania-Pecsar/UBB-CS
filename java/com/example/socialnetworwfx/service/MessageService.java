package com.example.socialnetworwfx.service;

import com.example.socialnetworwfx.domain.Message;
import com.example.socialnetworwfx.domain.ReplyMessage;
import com.example.socialnetworwfx.domain.User;
import com.example.socialnetworwfx.domain.event.ChangeEventType;
import com.example.socialnetworwfx.domain.event.MessageEntityChange;
import com.example.socialnetworwfx.repository.MessageDbRepository;
import com.example.socialnetworwfx.utils.Observable;
import com.example.socialnetworwfx.utils.Observer;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.StreamSupport;

public class MessageService implements Observable<MessageEntityChange> {
    private MessageDbRepository messageRepository;
    private List<Observer<MessageEntityChange>> observers = new ArrayList<>();

    public MessageService(MessageDbRepository messageRepository) {

        this.messageRepository = messageRepository;
    }

    public Message sendMessage(User fromUser, List<User> toUsers, String messageText) {
        Message message = new Message(fromUser, toUsers, messageText, LocalDateTime.now());
        messageRepository.save(message);
        notifyObservers(new MessageEntityChange(ChangeEventType.ADD, message));
        return message;
    }

    public Message sendReplyMessage(User fromUser, List<User> toUsers, String messageText, Message originalMessage) {
        ReplyMessage replyMessage = new ReplyMessage(fromUser, toUsers, messageText, LocalDateTime.now(), originalMessage);
        messageRepository.save(replyMessage);
        notifyObservers(new MessageEntityChange(ChangeEventType.ADD, replyMessage));
        return replyMessage;
    }

    public Message save(User fromUser, List<User> toUsers, String messageText) {
        Message message = new Message(fromUser, toUsers, messageText, LocalDateTime.now());
        messageRepository.save(message).orElse(null);
        MessageEntityChange event = new MessageEntityChange(ChangeEventType.ADD,message);
        notifyObservers(event);

        return message;
    }

    public Message delete(Long messageId) {
        Message message = messageRepository.findOne(messageId).orElseThrow(() -> new IllegalArgumentException("Message not found"));
        messageRepository.delete(messageId);
        MessageEntityChange event = new MessageEntityChange(ChangeEventType.DELETE, message);
        notifyObservers(event);
        return message;
    }

    public Message update(Message message) {
        messageRepository.update(message);
        MessageEntityChange event = new MessageEntityChange(ChangeEventType.UPDATE, message);
        notifyObservers(event);
        return message;
    }

    public Iterable<Message> findAll() {
        return messageRepository.findAll();
    }

    public List<Message> findMessagesByUsers(Long currentUserId, Long friendId) {
        return StreamSupport.stream(messageRepository.findAll().spliterator(), false)
                .filter(message ->
                        (message.getFrom().getID().equals(currentUserId) && message.getTo().stream().anyMatch(user -> user.getID().equals(friendId))) ||
                                (message.getFrom().getID().equals(friendId) && message.getTo().stream().anyMatch(user -> user.getID().equals(currentUserId))))
                .collect(Collectors.toList());
    }

    @Override
    public void addObserver(Observer<MessageEntityChange> observer) {
        observers.add(observer);
        System.out.println("Observer adăugat: " + observer.getClass().getName());
    }

    @Override
    public void removeObserver(Observer<MessageEntityChange> observer) {
        //observers.remove(observer);
    }

    @Override
    public void notifyObservers(MessageEntityChange change) {
        observers.stream().forEach((x -> x.update(change)));
        System.out.println("Notificare trimisă către " + observers.size() + " observatori.");
    }
}
