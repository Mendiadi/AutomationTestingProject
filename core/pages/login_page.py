from core.pages.authorized_pages import AuthenticationPage
import allure
from selenium.webdriver.common.by import By
from core.pages.store_page import StorePage
from commons.utils import log_data


class LoginPage(AuthenticationPage):
    def __init__(self, driver):
        super().__init__(driver)

    _locators = {
        "register": (By.XPATH, '//*[@id="root"]/div/button')
    }

    def login(self, email: str, password: str) -> StorePage:
        log_data(email, password, msg="perform login")
        self.send_email(email)
        self.send_password(password)
        self.on_submit()
        return StorePage(self._driver)

    @allure.step("Click Register")
    def click_register(self):
        self._driver.locate_element(self._locators['register']).click()
        from core.pages.register_page import RegisterPage
        return RegisterPage(self._driver)

    def get_register_btn_text(self) -> str:
        btn = self._driver.locate_element(self._locators['register'])
        return self._driver.text(btn)

    def elements_visible_login(self):
        res = self.elements_visible()
        elem = self._driver.element_is_visible(self._locators['register'])
        res.append(str(elem))
        log_data(msg=f"elements visible login page -> {res}")
        return res
