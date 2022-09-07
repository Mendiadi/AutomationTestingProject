from api_source.api.book_api import BookApi
import pytest
import logging
import random
from commons import utils
from api_source.models.api_user_dto import ApiUserDto
from commons.utils import json_read
from api_source.core.rest import get_session
from api_source.api.authors_api import Authors

LOGGER = logging.getLogger(__name__)

URL = 'http://localhost:7017/api/'
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
def get_book_api(generate_token) -> BookApi:
    return BookApi(URL, HEADERS, generate_token)


@pytest.fixture(scope="session")
def fix_user():
    user = utils.json_read(r"data_api.json")
    return ApiUserDto(**user['main_user'])


@pytest.fixture(scope="session")
def authors_api(generate_token):
    return Authors(URL, HEADERS, generate_token)


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


def test_post_au(authors_api):
    res = authors_api.post_au(data={
        "name": "string",
        "homeLatitude": 0,
        "homeLongitude": 0
    })
    LOGGER.info(res)


def test_refresh_token(get_book_api, fix_user):
    api = get_book_api
    res = api.refresh_token(data={
        "userId": "string",
        "token": "string",
        "refreshToken": "string"
    })
    LOGGER.info(res)
