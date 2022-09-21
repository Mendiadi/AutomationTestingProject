import allure
from core.pages.authorized_pages import AuthenticationPage
from selenium.webdriver.common.by import By
from commons.utils import log_data


class RegisterPage(AuthenticationPage):

    def __init__(self, driver):
        super().__init__(driver)

    _locators = {
        "firstname_field": (By.ID, "firstName"),
        "lastname_field": (By.ID, "lastName"),
        "back_login": (By.XPATH, '//*[@id="root"]/div/button')
    }

    @allure.step("send firstname")
    def send_firstname(self, firstname: str):
        field = self._driver.locate_element(self._locators["firstname_field"])
        self._driver.send_keys(field, firstname)

    @allure.step("send lastname")
    def send_lastname(self, lastname: str):
        field = self._driver.locate_element(self._locators["lastname_field"])
        self._driver.send_keys(field, lastname)

    def register(self, email: str, password: str, firstname: str, lastname: str):
        log_data(email, password, firstname, lastname, msg="perform register -> ")
        with allure.step(f" register with - {email},{password},{firstname},{lastname}"):
            self.send_email(email)
            self.send_password(password)
            self.send_firstname(firstname)
            self.send_lastname(lastname)
            self.on_submit()

    @allure.step("click back to login")
    def click_back_login(self):
        from core.pages.login_page import LoginPage
        btn = self._driver.locate_element(self._locators["back_login"])
        btn.click()
        return LoginPage(self._driver)

    def get_back_login_btn_text(self) -> str:
        btn = self._driver.locate_element(self._locators["back_login"])
        return self._driver.text(btn)

    def element_visible_register(self):
        res = self.elements_visible()
        for locator in self._locators.values():
            isfound = self._driver.element_is_visible(locator)
            res.append(str(isfound))
        log_data(msg=f"elements visible register -> {res}")
        return res
