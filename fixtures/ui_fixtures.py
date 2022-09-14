import os
import ctypes
import pytest
import allure
from playwright.sync_api import sync_playwright
from selenium import webdriver
from core.pages.login_page import LoginPage
from commons import load_test_data
from core.drivers import Driver





@pytest.fixture
def get_test_data(pytestconfig):
    data = load_test_data()
    data.url = pytestconfig.getoption("url")
    data.lib = pytestconfig.getoption("lib")
    data.browser = pytestconfig.getoption("browser")
    return data


# java -jar selenium-server-standalone-3.141.59.jar
@pytest.fixture
def init_driver(get_test_data, request):
    get_test_data.valid()
    if get_test_data.lib == "selenium":
        if get_test_data.selenium_grid:
            # 'http://127.0.0.1:4444/wd/hub'

            chrome_options = webdriver.ChromeOptions()

            page = webdriver.Remote(
                command_executor='http://localhost:4444/wd/hub',
                options=chrome_options
            )
            page.get(get_test_data.url)
        else:
            if get_test_data.browser == "chrome":
                page = webdriver.Chrome(get_test_data.driver_path)
            elif get_test_data.browser == "firefox":

                page = webdriver.Firefox(get_test_data.driver_path)
            page.get(get_test_data.url)
        page.maximize_window()
        obj_driver = Driver.create_driver(get_test_data.lib, page)
        yield obj_driver

    elif get_test_data.lib == "playwright":
        user32 = ctypes.windll.user32

        with sync_playwright() as p:
            if get_test_data.browser == "chrome":
                driver = p.chromium.launch(headless=False)
            elif get_test_data.browser == "firefox":
                driver = p.firefox.launch(headless=False)
            page = driver.new_page()
            page.goto(get_test_data.url)
            screensize = {"width": user32.GetSystemMetrics(0), "height": user32.GetSystemMetrics(1)}
            page.set_viewport_size(viewport_size=screensize)
            obj_driver = Driver.create_driver(get_test_data.lib, page)
            yield obj_driver
            play_w_img = obj_driver.get_screenshot()
            page.close()

    if request.node.rep_call.failed:
        try:
            if obj_driver.type == "selenium":
                obj_driver.script_execute("document.body.bgColor = 'white';")
                allure.attach(obj_driver.get_screenshot(),
                              name=request.function.__name__,
                              attachment_type=allure.attachment_type.PNG)
            else:
                allure.attach(play_w_img, attachment_type=allure.attachment_type.PNG)
                if "img.png" in os.listdir():
                    os.remove(play_w_img)
        except:
            pass
        finally:
            if obj_driver.type == "selenium":
                page.close()


@pytest.fixture
def get_main_page(init_driver):
    page = LoginPage(init_driver)
    yield page
    del page
