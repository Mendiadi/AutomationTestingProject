import pytest
from pages import main_page


@pytest.fixture
def get_main_page(init_driver):
    page = main_page.MainPage(init_driver)
    yield page
    del page

def test_search(get_main_page):
    get_main_page.search("hello world")

