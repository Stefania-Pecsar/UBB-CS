package com.example.socialnetworwfx.controller;

import com.example.socialnetworwfx.domain.Friendship;
import com.example.socialnetworwfx.domain.FriendshipRequest;
import com.example.socialnetworwfx.domain.User;
import com.example.socialnetworwfx.domain.event.FriendshipEntityChange;
import com.example.socialnetworwfx.repository.Paginare.Page;
import com.example.socialnetworwfx.service.FriendshipRequestService;
import com.example.socialnetworwfx.service.FriendshipService;
import com.example.socialnetworwfx.service.MessageService;
import com.example.socialnetworwfx.service.UserService;
import com.example.socialnetworwfx.utils.Observer;
import javafx.beans.property.SimpleStringProperty;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.layout.AnchorPane;
import javafx.stage.Stage;

import java.io.IOException;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.StreamSupport;

public class MainMenuView implements Observer<FriendshipEntityChange> {
    @FXML
    public TableColumn firstnameColumn;
    @FXML
    public TableView tableView;
    @FXML
    public TableColumn lastnameColumn;
    @FXML
    public Button sendRequestButton;
    @FXML
    public Button acceptRequestButton;
    @FXML
    public TableColumn<User, String> sinceColumn;
    @FXML
    public Button removeFriendButton;
    @FXML
    public Button removeUser;
    @FXML
    public Button accountSettingsButton;
    @FXML
    public Label userNameField;
    @FXML
    public Button messageButton;
    @FXML
    private Button nextButton;
    @FXML
    private Button previousButton;
    @FXML
    private Label currentPageLabel;


    private Long IDUser;
    private UserService userService;
    private FriendshipService friendshipService;
    private FriendshipRequestService requestService;
    private MessageService messageService;
    private Stage stage;
    private int currentPage = 0;
    private static final int PAGE_SIZE = 3;
    ObservableList<User> model = FXCollections.observableArrayList();

    public void setService(Long IDUser, UserService userService, FriendshipService friendshipService, FriendshipRequestService requestService, MessageService messageService, Stage stage) {
        this.IDUser = IDUser;
        this.userService = userService;
        this.friendshipService = friendshipService;
        this.requestService = requestService;
        this.messageService = messageService;
        this.stage = stage;
        friendshipService.addObserver(this);
        initModel();
    }

    public void initialize() {
        firstnameColumn.setCellValueFactory(new PropertyValueFactory<User, String>("firstName"));
        lastnameColumn.setCellValueFactory(new PropertyValueFactory<User, String>("lastName"));

        sinceColumn.setCellValueFactory(cellData -> {
            Long friendId = cellData.getValue().getID();
            Friendship friendship = friendshipService.findOne(friendId, IDUser);
            if (friendship == null) {
                friendship = friendshipService.findOne(IDUser, friendId);
            }
            return new SimpleStringProperty(friendship != null ? friendship.getDatesince().toString() : "Unknown");
        });

        tableView.setItems(model);
    }



    private void initModel() {
        Page<User> page = friendshipService.getPaginatedFriendships(IDUser, currentPage, PAGE_SIZE);
        List<User> allUsers = StreamSupport.stream(page.getElementsOnPage().spliterator(), false)
                .collect(Collectors.toList());

        model.setAll(allUsers);
        setUser(IDUser);

        int numberOfPages = (int) Math.ceil((double) page.getTotalNrOfElems() / PAGE_SIZE);
        currentPageLabel.setText("Page " + (currentPage + 1) + " of " + numberOfPages);

        nextButton.setDisable(currentPage + 1 == numberOfPages);
        previousButton.setDisable(currentPage == 0);
    }


    public void onNextPage(ActionEvent actionEvent) {
        currentPage++;
        initModel();
    }

    private void updatePageLabel(int currentPage, int totalPages) {
        currentPageLabel.setText("Page " + (currentPage + 1) + " of " + totalPages);
    }

    public void onPreviousPage(ActionEvent actionEvent) {
        if (currentPage > 0) {
            currentPage--;
            initModel();
        }
    }

    private void initPage() {
        initModel();
        int totalPages = (int) Math.ceil((double) model.size() / PAGE_SIZE);
        updatePageLabel(currentPage, totalPages);
    }

    public void setUser(Long IDUser) {
        User user = userService.findOne(IDUser);
        String fullName=user.getFirstName()+" "+user.getLastName();
        userNameField.setText(fullName);
    }

    public void handleSendRequest(ActionEvent actionEvent) throws IOException {
        FXMLLoader loader = new FXMLLoader();
        loader.setLocation(getClass().getResource("../request-view.fxml"));

        AnchorPane root = (AnchorPane) loader.load();
        Scene scene = new Scene(root);
        Stage stage2 = new Stage();
        stage2.setScene(scene);
        stage2.setTitle("Yahoo Messenger");

        RequestView requestView = loader.getController();
        requestView.setService(requestService, userService, IDUser);
        stage2.show();
    }

    public void handleAcceptRequest(ActionEvent actionEvent) throws IOException {
        FXMLLoader loader = new FXMLLoader();
        loader.setLocation(getClass().getResource("../accept-request.fxml"));

        AnchorPane root = (AnchorPane) loader.load();
        Scene scene = new Scene(root);
        Stage stage2 = new Stage();
        stage2.setScene(scene);
        stage2.setTitle("Yahoo Messenger");

        AcceptRequest requestView = loader.getController();
        requestView.setService(requestService, userService, friendshipService, IDUser);
        stage2.show();
    }

    public void handleMessageButton(ActionEvent actionEvent) throws IOException {
        User selectedUser = (User)tableView.getSelectionModel().getSelectedItem();

        if (selectedUser == null) {
            System.out.println("No friend selected to message.");
            return;
        }

        FXMLLoader loader = new FXMLLoader();
        loader.setLocation(getClass().getResource("../chat-view.fxml"));

        AnchorPane root = loader.load();
        Scene scene = new Scene(root);
        Stage stage2 = new Stage();
        stage2.setScene(scene);
        stage2.setTitle("Chat with " + selectedUser.getFirstName() + " " + selectedUser.getLastName());

        ChatView chatView = loader.getController();
        if (chatView == null) {
            System.err.println("Error: ChatView controller is null!");
            return;
        }
        System.out.println("MessageService before setting in ChatView: " + messageService);
        chatView.setService(messageService, userService, IDUser, selectedUser);

        stage2.show();
    }

    @Override
    public void update(FriendshipEntityChange friendshipEntityChange) {
        initModel();
    }

    public void handleRemoveFriend(ActionEvent actionEvent) {
        User request = (User) tableView.getSelectionModel().getSelectedItem();
        System.out.println(request.getID());
        Friendship friendship = friendshipService.findOne(request.getID(), IDUser);
        System.out.println(friendship.getID());
        FriendshipRequest friendshipRequest=requestService.findByIDs(IDUser,request.getID());
        System.out.println(friendshipRequest.getID());
        requestService.delete(friendshipRequest.getID());
        friendshipService.delete(friendship.getID());

    }


    public void handleRemoveUser(ActionEvent actionEvent) {
        User user = userService.findOne(IDUser);
    }

    public void handleAccountSetting(ActionEvent actionEvent) {

    }
}
