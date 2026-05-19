module com.example.socialnetworwfx {
    requires javafx.controls;
    requires javafx.fxml;
    requires java.sql;
    requires jdk.jfr;
    requires java.desktop;


    opens com.example.socialnetworwfx to javafx.fxml;
    exports com.example.socialnetworwfx;
}