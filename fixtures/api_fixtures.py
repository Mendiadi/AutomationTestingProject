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
    userid = user['main_user_id']
    return {"user": ApiUserDto(**user['main_user']), "userid": userid}

@pytest.fixture(scope="session")
def fix_admin_user():
    user = utils.json_read(r"data_api.json")
    return  LoginDto(**user['admin'])

@pytest.fixture(scope="session")
def url(pytestconfig):
    url = pytestconfig.getoption("url")
    url = url[:-1:]
    return url

@pytest.fixture(scope="session")
def bearer_au_session(fix_user,url):

    user_dict = fix_user['user'].to_json()
    with rest.Session() as new_session:
        code = rest.update_token(user_dict, new_session, f'{url}{URL_SWAGGER}{ACCOUNT_URL}/login')
        if code == 401:
            new_session.post(f'{url}{URL_SWAGGER}{ACCOUNT_URL}/register', json=user_dict)
            rest.update_token(user_dict, new_session, f'{URL}{ACCOUNT_URL}/login')
        yield new_session


@pytest.fixture(scope="session")
def get_account_api(bearer_au_session,url) -> AccountApi:
    url = url + URL_SWAGGER + ACCOUNT_URL
    session = bearer_au_session
    return AccountApi(url, session)

@pytest.fixture(scope="session")
def book_api(bearer_au_session,url):
    url = url + URL_SWAGGER +"Books"
    return BookApi(url,bearer_au_session)

@pytest.fixture(scope="session")
def authors_api(bearer_au_session,url):
    url = url + URL_SWAGGER +   AUTHORS_URL
    session = bearer_au_session
    return AuthorsApi(url, session)
