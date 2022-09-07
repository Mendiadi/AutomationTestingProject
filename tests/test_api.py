from api_source.api.book_api import BookApi
import pytest
import logging
from api_source.core import utils
from api_source.models.api_user_dto import ApiUserDto
LOGGER = logging.getLogger(__name__)

URL = 'http://localhost:7017/api/'
HEADERS = {'accept': 'application/json'}


@pytest.fixture(scope="session")
def get_book_api() -> BookApi:
    return BookApi(URL, HEADERS)

@pytest.fixture(scope="session")
def fix_user():
    user = utils.json_read(r"data_api.json")
    return ApiUserDto(**user)

#############################################
###########    INVALID CASES    #############
#############################################

def test_register(get_book_api,fix_user):
    api = get_book_api
    user = fix_user
    LOGGER.info(user.to_json())
    res = api.register(data=user.to_json())
    LOGGER.info(res)

    # assert res['code'] == 200

def test_register_exists_user(get_book_api,fix_user):
    api = get_book_api
    user = fix_user
    res = api.register(data=user.to_json())
    LOGGER.info(res)
    assert res['code'] == 400 and "DuplicateUserName" in res['msg']

def test_login(get_book_api,fix_user):
    api = get_book_api
    res = api.login(data={"email": "adi@sela.co.il", "password": "string11",})
    LOGGER.info(res.userId)



def test_refresh_token(get_book_api,fix_user):
    api = get_book_api
    res = api.refresh_token(data={
  "userId": "string",
  "token": "string",
  "refreshToken": "string"
})
    LOGGER.info(res)