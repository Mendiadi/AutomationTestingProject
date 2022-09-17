import os
import pytest
import allure
from core.pages.login_page import LoginPage
from commons import load_test_data
from commons.constant import *
from core.drivers import DriverContextManager


@pytest.fixture(scope="session")
def get_test_data(pytestconfig):
    data = load_test_data()
    data.url = pytestconfig.getoption("url")
    data.lib = pytestconfig.getoption("lib")
    data.browser = pytestconfig.getoption("browser")
    data.selenium_grid = pytestconfig.getoption("grid")
    return data


@pytest.fixture
def init_driver(get_test_data, request):
    get_test_data.valid()
    with DriverContextManager(get_test_data) as d:
        driver = d.init()
        yield driver
        if request.node.rep_call.failed:
            try:
                if driver.type == SELENIUM:
                    driver.script_execute("document.body.bgColor = 'white';")
                    allure.attach(driver.get_screenshot(),
                                  name=request.function.__name__,
                                  attachment_type=allure.attachment_type.PNG)
                else:
                    play_w_img = driver.get_screenshot()
                    allure.attach(play_w_img, attachment_type=allure.attachment_type.PNG)
                    if IMG_PLAYWRIGHT in os.listdir("..") or IMG_PLAYWRIGHT in os.listdir():
                        os.remove(IMG_PLAYWRIGHT)
            except:
                pass



@pytest.fixture
def main_page(init_driver):
    page = LoginPage(init_driver)
    yield page
    del page
