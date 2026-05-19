package demo.pages;

import net.serenitybdd.core.pages.PageObject;
import net.thucydides.core.annotations.DefaultUrl;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;

@DefaultUrl("https://scs.ubbcluj.ro/vvta/net2ftp/index.php")
public class Net2ftpPage extends PageObject {

    @FindBy(name = "ftpserver")
    private WebElement ftpServerField;

    @FindBy(name = "username")
    private WebElement usernameField;

    @FindBy(name = "password")
    private WebElement passwordField;

    @FindBy(css = "input[type='submit']")
    private WebElement loginButton;

    public void enterFtpServer(String server) {
        ftpServerField.clear();
        ftpServerField.sendKeys(server);
    }

    public void enterUsername(String username) {
        usernameField.clear();
        usernameField.sendKeys(username);
    }

    public void enterPassword(String password) {
        passwordField.clear();
        passwordField.sendKeys(password);
    }

    public void clickLogin() {
        loginButton.click();
    }

    public boolean isLoginSuccessful() {
        // Verifică că după login apare un element specific paginii de după autentificare
        // Inspectează pagina și ajustează selectorul
        return getDriver().getPageSource().contains("logout") ||
                getDriver().getPageSource().contains("Log out");
    }

    public boolean isLoginFailed() {
        return getDriver().getPageSource().contains("error") ||
                getDriver().getPageSource().contains("incorrect") ||
                getDriver().getPageSource().contains("Wrong");
    }
}