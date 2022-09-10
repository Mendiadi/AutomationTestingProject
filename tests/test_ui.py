import logging
import time

import allure
from commons.generate_data import RandomData

LOGGER = logging.getLogger(__name__)

@allure.epic("UI Readability")
class TestReadability:


    @allure.title("verify buttons readability")
    def test_readability_of_buttons(self, get_main_page):
        submit_btn_text = get_main_page.get_submit_btn_text()
        register_btn_text = get_main_page.get_register_btn_text()
        register_page = get_main_page.click_register()
        back_to_login_text = register_page.get_back_login_btn_text()
        assert submit_btn_text == "Submit"
        assert register_btn_text == "Register!"
        assert back_to_login_text == "Back To Login"


@allure.epic("UI Authentication system")
class TestAuthentication:
    data = RandomData()

    @allure.title("verify open page")
    def test_page_open(self, get_main_page):
        LOGGER.info(f"executing test case: search valid")
        excepted_title = "React App"
        LOGGER.info(f"actual: {get_main_page.title} | excepted: {excepted_title}")
        assert get_main_page.title == excepted_title

    @allure.feature("Feature: Login")
    @allure.title("verify Login")
    def test_login(self, get_main_page,get_test_data):
        LOGGER.info("login valid")
        store_page = get_main_page.login(get_test_data.email, get_test_data.password)
        time.sleep(5)
        text = store_page.get_label_h1_text()
        LOGGER.info(text)
        assert text == 'Welcome to our store'

    @allure.feature("Feature: Register")
    @allure.title("verify register")
    def test_register(self, get_main_page):
        register_page = get_main_page.click_register()
        register_page.register(self.data.email(), self.data.password(), self.data.firstname(), self.data.lastname())


