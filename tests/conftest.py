import pytest
from ui_source.core.drivers.driver import Driver
from playwright.sync_api import sync_playwright
from selenium.webdriver import Chrome, Firefox
from ui_source.core.common.data_load import  load_test_data
from ui_source.core.common.constant import DATA_FILE
import allure


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


def pytest_addoption(parser):
    data = load_test_data()
    parser.addoption("--url", action="store", default=data.url)
    parser.addoption("--lib", action="store", default=data.lib)
    parser.addoption("--browser", action="store", default=data.browser)


@pytest.fixture
def get_test_data(pytestconfig):
    data =  load_test_data()
    data.url = pytestconfig.getoption("url")
    data.lib = pytestconfig.getoption("lib")
    data.browser = pytestconfig.getoption("browser")
    return data


@pytest.fixture
def init_driver(get_test_data, request):
    get_test_data.valid()
    if get_test_data.lib == "selenium":
        if get_test_data.browser == "chrome":
            page = Chrome(get_test_data.driver_path)
        elif get_test_data.browser == "firefox":
            page = Firefox(get_test_data.driver_path)
        page.get(get_test_data.url)
        yield Driver.create_driver(get_test_data.lib, page)
        page.close()
    elif get_test_data.lib == "playwright":
        with sync_playwright() as p:
            if get_test_data.browser == "chrome":
                page = p.chromium.launch(headless=False)
            elif get_test_data.browser == "firefox":
                page = p.firefox.launch(headless=False)
            new_page = page.new_page()
            new_page.goto(get_test_data.url)
            yield Driver.create_driver(get_test_data.lib, new_page)
            new_page.close()
    if request.node.rep_call.failed:
        try:
            init_driver.script_execute("document.body.bgColor = 'white';")
            allure.attach(init_driver.get_screenshot(),
                          name=request.function.__name__,
                          attachment_type=allure.attachment_type.PNG)

        except:

            pass
