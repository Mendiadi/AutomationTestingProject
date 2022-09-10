from ui_source.pages.authorized_pages import AutenticationPage
import allure
from selenium.webdriver.common.by import By
from ui_source.pages import store_page

class LoginPage(AutenticationPage):
    def __init__(self, driver):
        super().__init__(driver)

    _locators = {
        "register": (By.XPATH, '//*[@id="root"]/div/button')
    }

    def login(self, email: str, password: str):
        self.send_email(email)
        self.send_password(password)
        self.on_submit()
        return store_page.StorePage(self._driver)

    @allure.step("Click Register")
    def click_register(self):
        self._driver.locate_element(self._locators['register']).click()
        from ui_source.pages.register_page import RegisterPage
        return RegisterPage(self._driver)

    def get_register_btn_text(self) -> str:
        btn = self._driver.locate_element(self._locators['register'])
        return self._driver.text(btn)
