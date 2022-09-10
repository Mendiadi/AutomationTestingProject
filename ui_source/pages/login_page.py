from ui_source.pages.base_page import BasePage
import allure
from selenium.webdriver.common.by import By


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    _locators = {
        "email_entry": (By.ID, 'email'),
        "password_entry": (By.ID, 'password'),
        "submit": (By.XPATH, '//*[@id="root"]/div/form/button'),
        "register":(By.XPATH,'//*[@id="root"]/div/button')
    }
    @allure.step("Sending Email")
    def send_email(self, email: str):
        email_entry = self._driver.locate_element(self._locators["email_entry"])
        self._driver.send_keys(email_entry, email)

    @allure.step("Sending PASS")
    def send_password(self, password: str):
        password_entry = self._driver.locate_element(self._locators["password_entry"])
        self._driver.send_keys(password_entry, password)

    @allure.step("Click Submit")
    def on_submit(self):
        self._driver.locate_element(self._locators["submit"]).click()


    def login(self, email: str, password: str):
        self.send_email(email)
        self.send_password(password)
        self.on_submit()

    @allure.step("Click Register")
    def click_register(self):

        self._driver.locate_element(self._locators['register']).click()


    def register(self):
        self.click_register()