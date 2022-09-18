from core.pages.base_page import BasePage
from selenium.webdriver.common.by import By
import allure



class AuthenticationPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    _au_locators = {
        "email_entry": (By.ID, 'email'),
        "password_entry": (By.ID, 'password'),
        "submit": (By.XPATH, '//*[@id="root"]/div/form/button'),

    }

    @allure.step("Sending Email")
    def send_email(self, email: str):
        email_entry = self._driver.locate_element(self._au_locators["email_entry"])
        self._driver.send_keys(email_entry, email)

    @allure.step("Sending PASS")
    def send_password(self, password: str):
        password_entry = self._driver.locate_element(self._au_locators["password_entry"])
        self._driver.send_keys(password_entry, password)

    @allure.step("Click Submit")
    def on_submit(self):
        self._driver.locate_element(self._au_locators["submit"]).click()

    def get_submit_btn_text(self) -> str:
        btn = self._driver.locate_element(self._au_locators['submit'])
        return self._driver.text(btn)

    def elements_visible(self) -> list[...]:
        results = []
        for locator in self._au_locators.values():
            is_found = self._driver.element_is_visible(locator)
            results.append(is_found)
        return results

    def get_email_placeholder(self) -> str:
        field = self._driver.locate_element(self._au_locators['email_entry'])
        return self._driver.get_attribute(field,"placeholder")

    def get_password_placeholder(self) -> str:
        field = self._driver.locate_element(self._au_locators['password_entry'])
        return self._driver.get_attribute(field, "placeholder")