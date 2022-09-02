import pytest
from common.supports import create_driver
from playwright.sync_api import sync_playwright
from selenium import webdriver
from common import test_data
from common.constant import DATA_FILE


@pytest.fixture
def get_test_data():
    return test_data.TestsData.load(DATA_FILE)


@pytest.fixture
def init_driver(get_test_data):
    if get_test_data.lib == "selenium":
        if get_test_data.browser == "chrome":
            page = webdriver.Chrome(get_test_data.driver_path)
        elif get_test_data.browser == "firefox":
            page = webdriver.Firefox(get_test_data.driver_path)
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
