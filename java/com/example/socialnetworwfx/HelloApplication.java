package com.example.socialnetworwfx;

import com.example.socialnetworwfx.controller.LoginView;
import com.example.socialnetworwfx.domain.validation.FriendshipValidation;
import com.example.socialnetworwfx.domain.validation.MessageValidation;
import com.example.socialnetworwfx.domain.validation.RequestValidation;
import com.example.socialnetworwfx.domain.validation.UserValidation;
import com.example.socialnetworwfx.repository.FriendshipDbRepository;
import com.example.socialnetworwfx.repository.FriendshipRequestDbRepository;
import com.example.socialnetworwfx.repository.MessageDbRepository;
import com.example.socialnetworwfx.repository.UserDbRepository;
import com.example.socialnetworwfx.service.FriendshipRequestService;
import com.example.socialnetworwfx.service.FriendshipService;
import com.example.socialnetworwfx.service.MessageService;
import com.example.socialnetworwfx.service.UserService;
import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.layout.AnchorPane;
import javafx.stage.Stage;
import javafx.scene.image.Image;
import java.awt.*;
import java.io.IOException;
import java.sql.SQLException;
import java.util.Objects;

public class HelloApplication extends Application {
    UserDbRepository userRepository;
    FriendshipDbRepository friendshipRepository;
    UserService userService;
    FriendshipService friendshipService;
    FriendshipRequestDbRepository friendshipRequestDbRepository;
    FriendshipRequestService friendshipRequestService;
    MessageDbRepository messageRepository;
    MessageService messageService;

    @Override
    public void start(Stage primaryStage) throws IOException, SQLException {
        String username = "postgres";
        String password = "stefania20043";
        String url = "jdbc:postgresql://localhost:5432/postgres";
        userRepository = new UserDbRepository(url,username,password, new UserValidation());
        friendshipRepository = new FriendshipDbRepository(url,username, password, new FriendshipValidation());
        userService = new UserService(userRepository);
        friendshipService=new FriendshipService(friendshipRepository,userRepository);
        friendshipRequestDbRepository=new FriendshipRequestDbRepository(url,username,password,new RequestValidation());
        friendshipRequestService=new FriendshipRequestService(friendshipRequestDbRepository,userService);
        messageRepository = new MessageDbRepository(url, username, password,new MessageValidation(),userRepository);
        messageService = new MessageService(messageRepository);

        initView(primaryStage);
        primaryStage.setWidth(600);
        primaryStage.show();
    }

    private void initView(Stage primaryStage) throws IOException {

        FXMLLoader fxmlLoader = new FXMLLoader(HelloApplication.class.getResource("login-view.fxml"));

        AnchorPane userLayout = fxmlLoader.load();
        primaryStage.setScene(new Scene(userLayout));
        primaryStage.setTitle("Yahoo Messenger");
        LoginView loginController = fxmlLoader.getController();
        loginController.setService(userService,friendshipService,friendshipRequestService,messageService);

    }

    public static void main(String[] args) {
        launch();
    }
}