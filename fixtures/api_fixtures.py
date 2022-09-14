from api_source.api.account_api import AccountApi
from commons import utils
from api_source.models.api_user_dto import ApiUserDto
from api_source.core import rest
from api_source.api.authors_api import AuthorsApi
from api_source.core.constant import *
from commons.generate_data import RandomData
from api_source.api.book_api import BookApi
from api_source.models.login_dto import LoginDto
import pytest


@pytest.fixture(scope="session")
def random_data():
    return RandomData()


@pytest.fixture(scope="session")
def fix_user():
    user = utils.json_read(r"data_api.json")
    user_id = utils.json_read(r"user_id.json")
    return {"user": ApiUserDto(**user['main_user']), "userid": user_id['id']}


@pytest.fixture(scope="session")
def fix_admin_user():
    user = utils.json_read(r"data_api.json")
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
