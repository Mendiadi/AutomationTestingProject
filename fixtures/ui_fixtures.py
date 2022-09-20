import os
import pytest
import allure
from core.pages.login_page import LoginPage
from commons import TestsData
from commons.constant import *
from core.drivers import DriverContextManager, Driver


@pytest.fixture(scope="session")
def configuration(pytestconfig):
    data = TestsData.load(DATA_FILE)
    data.url = pytestconfig.getoption("url")
    data.lib = pytestconfig.getoption("lib")
    data.browser = pytestconfig.getoption("browser")
    data.selenium_grid = pytestconfig.getoption("grid")
    data.valid()
    return data


@pytest.fixture
def init_driver(configuration, request) -> Driver:
    with DriverContextManager(configuration) as driver:
        page = driver.activate()
        yield page
        if request.node.rep_call.failed:
            try:
                page.script_execute("document.body.bgColor = 'white';")
                allure.attach(page.get_screenshot(),
                              name=request.function.__name__,
                              attachment_type=allure.attachment_type.PNG)
            except:
                pass
        if IMG_PLAYWRIGHT in os.listdir("..") or IMG_PLAYWRIGHT in os.listdir():
            os.remove(IMG_PLAYWRIGHT)


@pytest.fixture
def main_page(init_driver, api):
    page = LoginPage(init_driver)
    yield page
    del page


@pytest.fixture(scope="class")
def safe_load(api):
    print("start")
    yield
    print("done")
    authors = api.authors.get_authors()
    for author in authors:
        if author.id > 5:
            api.authors.delete_author(id=author.id)


@pytest.fixture(scope="class")
def book_setup(api, data, request):
    author_created = data.generate_author()
    author = api.authors.post_authors(author_created)
    book_created = data.generate_book(authorid=author.id, imageUrl=True)
    book = api.books.post_books(book_created)
    request.cls.book = book
    yield
    api.authors.delete_author(id=author.id)


@pytest.fixture(scope="class")
def author_setup(api, data, request):
    author = api.authors.post_authors(data.generate_author(la=31.343, lo=33.345))
    request.cls.author = author
    yield
    api.authors.delete_author(id=author.id)


@pytest.fixture(scope="class")
def author_setup2(api, data, request, fix_user):
    res = api.account.login(fix_user['user'].to_json())
    api.session.update_token(res.token)
    author = api.authors.post_authors(data.generate_author(name="mr no name"))
    request.cls.author2 = author
    yield
    api.authors.delete_author(id=author.id)


@pytest.fixture(scope="class")
def author_setup1(api, data, request, fix_user):
    res = api.account.login(fix_user['user'].to_json())
    api.session.update_token(res.token)
    author = api.authors.post_authors(data.generate_author())
    request.cls.author1 = author
    yield
    api.authors.delete_author(id=author.id)
