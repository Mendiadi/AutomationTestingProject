import pytest
from core import rest
from core.api import AccountApi
from core.api import BookApi
from core.api import AuthorsApi
from core.api.constant import *
from commons import json_read
from commons import RandomData
from core.models import LoginDto
from core.models import ApiUserDto




@pytest.fixture(scope="session")
def random_data():
    return RandomData()


@pytest.fixture(scope="session")
def fix_user():
    user = json_read(r"data_api.json")
    user_id = json_read(r"user_id.json")
    return {"user": ApiUserDto(**user['main_user']), "userid": user_id['id']}


@pytest.fixture(scope="session")
def fix_admin_user():
    user = json_read(r"data_api.json")
    return LoginDto(**user['admin'])


@pytest.fixture(scope="session")
def url(pytestconfig):
    url = pytestconfig.getoption("url")
    url = url[:-1:]
    return url


@pytest.fixture(scope="session")
def bearer_au_session(fix_user, url, fix_admin_user):
    user_dict = {"user": fix_user['user'].to_json(), "main_user_id": fix_user['userid']}

    with rest.Session() as new_session:
        new_session.session.post(url=f"{url}{URL_SWAGGER}{ACCOUNT_URL}/register", json=ApiUserDto(
            fix_admin_user.email, fix_admin_user.password, "admin", "admin").to_json())
        new_session.set_login_url(f'{url}{URL_SWAGGER}{ACCOUNT_URL}/login')
        code = new_session.update_token(user_dict)
        if code == 401:
            new_session.session.post(f'{url}{URL_SWAGGER}{ACCOUNT_URL}/register', json=user_dict['user'])

            new_session.update_token(user_dict, True)
        yield new_session


@pytest.fixture(scope="session")
def get_account_api(bearer_au_session, url) -> AccountApi:
    url = url + URL_SWAGGER + ACCOUNT_URL
    session = bearer_au_session
    return AccountApi(url, session)


@pytest.fixture(scope="session")
def book_api(bearer_au_session, url):
    url = url + URL_SWAGGER + "Books"
    return BookApi(url, bearer_au_session)


@pytest.fixture(scope="session")
def authors_api(bearer_au_session, url):
    url = url + URL_SWAGGER + AUTHORS_URL
    session = bearer_au_session
    api = AuthorsApi(url, session)
    yield api
    authors = api.get_authors()
    for author in authors:
        if author.id > 3:
            api.delete_author(id=author.id)
