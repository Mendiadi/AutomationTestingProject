import pytest
from UI.common.supports import create_driver
from playwright.sync_api import sync_playwright
from selenium.webdriver import Chrome, Firefox
from UI.common import data_load
from UI.common.constant import DATA_FILE





def test_data():
    return data_load.TestsData.load(DATA_FILE)


def pytest_addoption(parser):
    data =  test_data()
    parser.addoption("--url", action="store", default=data.url)
    parser.addoption("--lib", action="store", default=data.lib)
    parser.addoption("--browser", action="store", default=data.browser)

@pytest.fixture
def get_test_data(pytestconfig):
    data = test_data()
    data.url = pytestconfig.getoption("url")
    data.lib = pytestconfig.getoption("lib")
    data.browser = pytestconfig.getoption("browser")
    return data



@pytest.fixture
def init_driver(get_test_data):
    get_test_data.valid()
    if get_test_data.lib == "selenium":
        if get_test_data.browser == "chrome":
            page = Chrome(get_test_data.driver_path)
        elif get_test_data.browser == "firefox":
            page = Firefox(get_test_data.driver_path)
        page.get(get_test_data.url)
        yield create_driver(get_test_data.lib, page)
        page.close()
    elif get_test_data.lib == "playwright":
        with sync_playwright() as p:
            if get_test_data.browser == "chrome":
                page = p.chromium.launch(headless=False)
            elif get_test_data.browser == "firefox":
                page = p.firefox.launch(headless=False)
            new_page = page.new_page()
            new_page.goto(get_test_data.url)
            yield create_driver(get_test_data.lib, new_page)
            new_page.close()
