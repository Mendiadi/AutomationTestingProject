import pytest
from ui_source.pages import login_page
from ui_source.core.data_load import load_test_data
from ui_source.core.drivers.driver import Driver
from playwright.sync_api import sync_playwright
from selenium import webdriver
from commons.utils import screenshot_if_failed


@pytest.fixture
def get_test_data(pytestconfig):
    data = load_test_data()
    data.url = pytestconfig.getoption("url")
    data.lib = pytestconfig.getoption("lib")
    data.browser = pytestconfig.getoption("browser")
    return data

#java -jar selenium-server-standalone-3.141.59.jar
@pytest.fixture
def init_driver(get_test_data, request):
    get_test_data.valid()
    if get_test_data.lib == "selenium":
        if get_test_data.selenium_grid:
            # 'http://127.0.0.1:4444/wd/hub'
            capabilities = webdriver.ChromeOptions()
            page =  webdriver.Remote(
                command_executor='http://localhost:4444/wd/hub',
                desired_capabilities={
                    'browserName':"Chrome",
                    'javascriptEnabled': True
                },options=capabilities
            )
            page.get(get_test_data.url )
        else:
            if get_test_data.browser == "chrome":


                page =  webdriver.Chrome(get_test_data.driver_path)
            elif get_test_data.browser == "firefox":


                page =  webdriver.Firefox(get_test_data.driver_path)
            page.get(get_test_data.url)
        page.maximize_window()
        yield Driver.create_driver(get_test_data.lib, page)
        screenshot_if_failed(page, request)
        page.close()
    elif get_test_data.lib == "playwright":
        with sync_playwright() as p:
            if get_test_data.browser == "chrome":
                driver = p.chromium.launch(headless=False)
            elif get_test_data.browser == "firefox":
                driver = p.firefox.launch(headless=False)
            page = driver.new_page()
            page.goto(get_test_data.url)
            screensize = {"width":1920, "height": 1080}
            page.set_viewport_size(viewport_size=screensize)
            yield Driver.create_driver(get_test_data.lib, page)
            screenshot_if_failed(page, request)
            page.close()


@pytest.fixture
def get_main_page(init_driver):
    page = login_page.LoginPage(init_driver)
    yield page
    del page