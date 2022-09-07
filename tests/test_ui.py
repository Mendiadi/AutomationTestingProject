import logging
import time
import pytest
from ui_source.pages import login_page

LOGGER = logging.getLogger(__name__)


@pytest.fixture
def get_main_page(init_driver):
    page = login_page.LoginPage(init_driver)
    yield page
    del page


def test_page_open(get_main_page):
    LOGGER.info(f"executing test case: search valid")
    excepted_title = "React App"
    LOGGER.info(f"actual: {get_main_page.title} | excepted: {excepted_title}")
    assert get_main_page.title == excepted_title


def test_login(get_main_page):
    LOGGER.info("login valid")
    get_main_page.login("adi@walla.c", "1111")


def test_press_book_store(get_main_page):
    get_main_page.click_bookstore()
    time.sleep(5)
