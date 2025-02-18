package com.example.socialnetworwfx.controller;

import com.example.socialnetworwfx.service.FriendshipRequestService;
import com.example.socialnetworwfx.service.UserService;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.stage.Stage;

public class RequestView {
    @FXML
    public Button sendButton;
    @FXML
    public Label failMessage;
    @FXML
    public TextField firstnameText;
    @FXML
    public TextField lastnameText;

    private FriendshipRequestService friendshipRequestService;
    private UserService userService;
    private Long ID;

    public void setService(FriendshipRequestService friendshipRequestService, UserService userService,Long ID){
        this.friendshipRequestService = friendshipRequestService;
        this.userService = userService;
        this.ID = ID;
    }


    public void handleSendButton(ActionEvent actionEvent) {
        String firstname = firstnameText.getText();
        String lastname = lastnameText.getText();
        System.out.println(firstname + " " + lastname);
        Long ID2=userService.findUserByNames(firstname,lastname);
        if(ID2!=null){
            friendshipRequestService.sendRequest(ID,ID2);
            failMessage.setVisible(false);
            firstnameText.clear();
            lastnameText.clear();
        }
        else{
            failMessage.setText("The request was not send!");
            failMessage.setVisible(true);
        }
    }
}

