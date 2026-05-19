package demo.steps.serenity;

import demo.pages.Net2ftpPage;
import net.thucydides.core.annotations.Step;
import org.junit.Assert;

public class LoginSteps {

    Net2ftpPage net2ftpPage;

    @Step
    public void navigateToLoginPage() {
        net2ftpPage.open();
    }

    @Step
    public void enterCredentials(String ftpServer, String username, String password) {
        net2ftpPage.enterFtpServer(ftpServer);
        net2ftpPage.enterUsername(username);
        net2ftpPage.enterPassword(password);
    }

    @Step
    public void clickLogin() {
        net2ftpPage.clickLogin();
    }

    @Step
    public void verifyLoginSuccess() {
        Assert.assertTrue("Login ar trebui să reușească cu date valide",
                net2ftpPage.isLoginSuccessful());
    }

    @Step
    public void verifyLoginFailure() {
        Assert.assertTrue("Login ar trebui să eșueze cu date invalide",
                net2ftpPage.isLoginFailed());
    }
}
