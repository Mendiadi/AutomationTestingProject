from api_source.api.account_api import AccountApi
from commons import utils
from api_source.models.api_user_dto import ApiUserDto
from api_source.core import rest
from api_source.api.authors_api import AuthorsApi
from api_source.core.constant import *
from commons.generate_data import RandomData
import pytest

@pytest.fixture(scope="session")
def random_data():
    return RandomData()


@pytest.fixture(scope="session")
def fix_user():
    user = utils.json_read(r"data_api.json")
    return ApiUserDto(**user['main_user'])


@pytest.fixture(scope="session")
def generate_token(fix_user):
    user_dict = fix_user.to_json()
    new_session = rest.get_session()
    res = new_session.post(url=f'http://localhost:7017/api/Account/login', json=user_dict)
    token = res.json()['token']
    headers = {'Authorization': f'Bearer {token}'}
    new_session.headers.update(headers)
    return new_session


@pytest.fixture(scope="session")
def generate_new_user(random_data):
    user = {
        "email": random_data.email(),
        "password": random_data.password(),
        "firstName": random_data.firstname(),
        "lastName": random_data.lastname()
    }
    return user


@pytest.fixture(scope="session")
def get_account_api(generate_token) -> AccountApi:
    url = URL + ACCOUNT_URL
    session = generate_token
    return AccountApi(url, session)


@pytest.fixture(scope="session")
def authors_api(generate_token):
    url = URL + AUTHORS_URL
    session = generate_token
    return AuthorsApi(url, session)