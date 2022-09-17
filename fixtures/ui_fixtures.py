import os
import pytest
import allure
from core.pages.login_page import LoginPage
from commons import load_test_data
from commons.constant import *
from core.drivers import DriverContextManager,Driver


@pytest.fixture(scope="session")
def get_test_data(pytestconfig):
    data = load_test_data()
    data.url = pytestconfig.getoption("url")
    data.lib = pytestconfig.getoption("lib")
    data.browser = pytestconfig.getoption("browser")
    data.selenium_grid = pytestconfig.getoption("grid")
    data.valid()
    return data


@pytest.fixture
def init_driver(get_test_data, request) -> Driver:
    with DriverContextManager(get_test_data) as d:
        driver = d.init()
        yield driver
        if request.node.rep_call.failed:
            try:
                driver.script_execute("document.body.bgColor = 'white';")
                allure.attach(driver.get_screenshot(),
                                name=request.function.__name__,
                                attachment_type=allure.attachment_type.PNG)
            except:
                pass
        if IMG_PLAYWRIGHT in os.listdir("..") or IMG_PLAYWRIGHT in os.listdir():
            os.remove(IMG_PLAYWRIGHT)


@pytest.fixture
def main_page(init_driver,api):
    page = LoginPage(init_driver)
    yield page
    del page

# @pytest.fixture(autouse=True)
# def safe_load(api):
#     authors =  api.authors.get_authors()
#     for author in authors:
#         api.authors.delete_author(id=author.id)

@pytest.fixture(scope="class")
def book_setup(api,data,request):
    author_created = data.generate_author()
    author = api.authors.post_authors(author_created)
    book_created = data.generate_book(authorid=author.id, imageUrl=True)
    book = api.books.post_books(book_created)
    request.cls.book = book
    yield
    api.authors.delete_author(id=author.id)

@pytest.fixture(scope="class")
def author_setup(api,data,request):
    author = api.authors.post_authors(data.generate_author(la=33.343, lo=34.345))
    request.cls.author = author
    yield
    api.authors.delete_author(id=author.id)
