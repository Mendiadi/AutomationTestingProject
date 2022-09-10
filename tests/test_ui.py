import logging
import allure
import pytest
from ui_source.pages import login_page
from ui_source.pages import register_page
from commons.generate_data import RandomData

LOGGER = logging.getLogger(__name__)

LOGGER.info("Starting executing UI tests")


@pytest.fixture
def get_main_page(init_driver):
    page = login_page.LoginPage(init_driver)
    yield page
    del page


@allure.epic("UI tests")
class TestUI:
    data = RandomData()

    @allure.title("verify open page")
    def test_page_open(self, get_main_page):
        LOGGER.info(f"executing test case: search valid")
        excepted_title = "React App"
        LOGGER.info(f"actual: {get_main_page.title} | excepted: {excepted_title}")
        assert get_main_page.title == excepted_title

    @allure.feature("Feature: Login")
    @allure.title("verify Login")
    def test_login(self, get_main_page):
        LOGGER.info("login valid")
        get_main_page.login("adi@walla.c", "1111")

    @allure.feature("Feature: Register")
    @allure.title("verify register")
    def test_register(self, get_main_page):
        register_page = get_main_page.click_register()
        register_page.register(self.data.email(), self.data.password(), self.data.firstname(), self.data.lastname())
