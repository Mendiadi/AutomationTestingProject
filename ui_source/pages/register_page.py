import allure
from ui_source.pages.authorized_pages import AutenticationPage
from selenium.webdriver.common.by import By


class RegisterPage(AutenticationPage):

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
        self.send_email(email)
        self.send_password(password)
        self.send_firstname(firstname)
        self.send_lastname(lastname)
        self.on_submit()

    def get_back_login_btn_text(self) -> str:
        btn = self._driver.locate_element(self._locators["back_login"])
        return self._driver.text(btn)