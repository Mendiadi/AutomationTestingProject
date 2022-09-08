from api_source.api.account_api import AccountApi
import pytest
import logging
import random
from commons import utils
from api_source.models.api_user_dto import ApiUserDto
from commons.utils import json_read
from api_source.core.rest import get_session
from api_source.api.authors_api import AuthorsApi
from api_source.core.constant import URL

LOGGER = logging.getLogger(__name__)

HEADERS = {'accept': 'application/json'}


@pytest.fixture(scope="session")
def generate_token():
    user = {
        "email": "adi@sela.co.il",
        "password": "string11",
        "firstName": "adi",
        "lastName": "mendel"
    }
    new_session = get_session(HEADERS)
    res = new_session.post(url='http://localhost:7017/api/Account/login', json=user)
    token = res.json()['token']
    headers = {'Authorization': f'Bearer {token}'}
    return get_session(headers)


@pytest.fixture(scope="session")
def generate_new_user():
    key = random.randint(0, 1000)
    data = json_read("data_api.json")
    new_user = data['new_user']
    new_user['email'] = new_user['email'].replace("%", str(key))
    return new_user


@pytest.fixture(scope="session")
def get_book_api(generate_token) -> AccountApi:
    url = URL + '/api/Account'
    return AccountApi(url, HEADERS, generate_token)


@pytest.fixture(scope="session")
def fix_user():
    user = utils.json_read(r"data_api.json")
    return ApiUserDto(**user['main_user'])


@pytest.fixture(scope="session")
def authors_api(generate_token):
    url = URL + '/api/Authors'
    return AuthorsApi(url, HEADERS, generate_token)


#############################################
###########    INVALID CASES    #############
#############################################

def test_register(get_book_api, generate_new_user):
    api = get_book_api
    user = generate_new_user
    LOGGER.info(user)
    res = api.register(data=user)
    LOGGER.info(res)
    assert res['code'] == 200


def test_register_exists_user(get_book_api, fix_user):
    api = get_book_api
    user = fix_user
    res = api.register(data=user.to_json())
    LOGGER.info(res)
    assert res['code'] == 400 and "DuplicateUserName" in res['msg']


def test_login(get_book_api, fix_user):
    api = get_book_api
    res = api.login(data={"email": "adi@sela.co.il", "password": "string11", })
    LOGGER.info(res.userId)


def test_post_authors(authors_api):
    author = authors_api.post_authors(data={"name": "adi", "homeLatitude": 0, "homeLongitude": 0})
    LOGGER.info(author)
    authors = authors_api.get_authors()
    assert author in authors
    authors_api.delete_author(id=author.id)


def test_delete_author(authors_api):
    api = authors_api
    author = api.post_authors(data={"name": "test", "homeLatitude": 0, "homeLongitude": 0})
    res = api.delete_author(id=author.id)
    LOGGER.info(res)
    authors = api.get_authors()
    assert author not in authors


def test_get_authors(authors_api):
    api = authors_api
    author = api.post_authors(data={"name": "david", "homeLatitude": 0, "homeLongitude": 0})
    authors = api.get_authors()
    LOGGER.info(authors)
    assert author in authors
    res = api.delete_author(id=author.id)
    LOGGER.info(res)
    authors = api.get_authors()
    assert author not in authors


def test_refresh_token(get_book_api, fix_user):
    api = get_book_api
    res = api.refresh_token(data=fix_user.to_json())
    LOGGER.info(res)
