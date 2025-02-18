package com.example.socialnetworwfx.controller;

import com.example.socialnetworwfx.domain.FriendshipRequest;
import com.example.socialnetworwfx.domain.Message;
import com.example.socialnetworwfx.domain.ReplyMessage;
import com.example.socialnetworwfx.domain.User;
import com.example.socialnetworwfx.domain.event.ChangeEventType;
import com.example.socialnetworwfx.domain.event.FriendshipEntityChange;
import com.example.socialnetworwfx.domain.event.MessageEntityChange;
import com.example.socialnetworwfx.service.MessageService;
import com.example.socialnetworwfx.service.UserService;

import com.example.socialnetworwfx.utils.Observer;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.scene.input.MouseEvent;
import javafx.stage.Stage;


import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.StreamSupport;

public class ChatView implements Observer<MessageEntityChange>{
    @FXML
    public TextArea conversationArea;
    @FXML
    public TextField messageContentText;
    @FXML
    public Button sendMessageButton;
    @FXML
    public Label errorMessage;
    @FXML
    public Label friendNameLabel;


    private MessageService messageService;
    private UserService userService;
    private Long currentUserId;
    private User selectedFriend;
    private Message selectedMessage;
    ObservableList<Message> model = FXCollections.observableArrayList();

    public void setService(MessageService messageService, UserService userService, Long currentUserId, User selectedFriend) {
        System.out.println("Setting service in ChatView instance: "+ this);
        this.messageService = messageService;
        this.userService = userService;
        this.currentUserId = currentUserId;
        this.selectedFriend = selectedFriend;
        friendNameLabel.setText(selectedFriend.getFirstName() + " " + selectedFriend.getLastName());
        messageService.addObserver(this);
        loadConversation();
        initModel();
    }


    private void loadConversation() {
        List<Message> messages = messageService.findMessagesByUsers(currentUserId, selectedFriend.getID());
        StringBuilder conversation = new StringBuilder();

        for (Message message : messages) {
            String timestamp = message.getData().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
            if (message instanceof ReplyMessage) {
                ReplyMessage reply = (ReplyMessage) message;
                conversation.append(" Replying to: ")
                        .append(reply.getReply().getMessage())
                        .append("\n");
            }
            conversation.append("[").append(timestamp).append("] ")
                    .append(message.getFrom().getFirstName()).append(": ")
                    .append(message.getMessage()).append("\n\n");
        }
        conversationArea.setText(conversation.toString());
    }


    public void handleSendMessage(ActionEvent event) {

        System.out.println("handleSendMessage called on instance: " + this);

        if (messageService == null) {
            System.err.println("messageService is null!");
            return;
        }

        String messageContent = messageContentText.getText();

        if (messageContent != null && !messageContent.isEmpty()) {
            try {
                messageService.sendMessage(userService.findOne(currentUserId), List.of(selectedFriend), messageContent);
                loadConversation();
                messageContentText.clear();
            } catch (Exception e) {
                e.printStackTrace();
                errorMessage.setText("Failed to send message!");
                errorMessage.setVisible(true);
            }
        } else {
            errorMessage.setText("Please enter a message.");
            errorMessage.setVisible(true);
        }
        initModel();
    }

    public void handleReplyMessage(ActionEvent event) {
        String messageContent = messageContentText.getText();
        if (selectedMessage != null && messageContent != null && !messageContent.isEmpty()) {
            try {
                messageService.sendReplyMessage(
                        userService.findOne(currentUserId),
                        List.of(selectedFriend),
                        messageContent,
                        selectedMessage
                );

                loadConversation();
                messageContentText.clear();

                selectedMessage = null;

                errorMessage.setVisible(false);
            } catch (Exception e) {
                e.printStackTrace();
                errorMessage.setText("Failed to send reply message!");
                errorMessage.setVisible(true);
            }
        } else if (selectedMessage == null) {
            errorMessage.setText("No message selected to reply to.");
            errorMessage.setVisible(true);
        } else if (messageContent == null || messageContent.isEmpty()) {

            errorMessage.setText("Please enter a reply message.");
            errorMessage.setVisible(true);
        }
        initModel();
    }

    private void initModel() {
        Iterable<Message> messages = messageService.findMessagesByUsers(currentUserId, selectedFriend.getID());
        List<Message> users = StreamSupport.stream(messages.spliterator(), false)
                .collect(Collectors.toList());
        model.setAll(users);
    }

    @Override
    public void update(MessageEntityChange messageEntityChange) {
        System.out.println("Update received in ChatView: " + messageEntityChange);
        initModel(); }

}