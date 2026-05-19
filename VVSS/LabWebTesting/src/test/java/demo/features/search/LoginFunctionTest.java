package demo.features.search;

import demo.steps.serenity.LoginSteps;
import net.serenitybdd.junit.runners.SerenityParameterizedRunner;
import net.thucydides.core.annotations.Issue;
import net.thucydides.core.annotations.Managed;
import net.thucydides.core.annotations.Steps;
import net.thucydides.junit.annotations.UseTestDataFrom;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.openqa.selenium.WebDriver;

@RunWith(SerenityParameterizedRunner.class)
@UseTestDataFrom("src/test/resources/features/search/LoginData.csv")
public class LoginFunctionTest {

    @Managed(uniqueSession = true)
    public WebDriver webdriver;

    @Steps
    public LoginSteps loginSteps;

    // Aceste variabile sunt populate automat din CSV (numele = header-ul din CSV)
    String ftp_server;
    String username;
    String password;
    String expected_result;

    @Issue("#WIKI-1")
    @Test
    public void login_with_valid_data_should_succeed() {
        if ("success".equals(expected_result)) {
            loginSteps.navigateToLoginPage();
            loginSteps.enterCredentials(ftp_server, username, password);
            loginSteps.clickLogin();
            loginSteps.verifyLoginSuccess();
        }
    }

    @Issue("#WIKI-2")
    @Test
    public void login_with_invalid_data_should_fail() {
        if ("failure".equals(expected_result)) {
            loginSteps.navigateToLoginPage();
            loginSteps.enterCredentials(ftp_server, username, password);
            loginSteps.clickLogin();
            loginSteps.verifyLoginFailure();
        }
    }
}