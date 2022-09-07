from api_source.api.book_api import BookApi
import pytest
import logging

LOGGER = logging.getLogger(__name__)

URL = "https://petstore3.swagger.io/api/v3/pet/"
HEADERS = {'accept': 'application/json'}
PET = {
    "id": 167,
    "name": "omg",
    "status": "available"
}


@pytest.fixture(scope="session")
def get_book_api() -> BookApi:
    return BookApi(URL, HEADERS)


def test_post_pet(get_book_api):
    api = get_book_api
    res = api.post_pet(data=PET)
    LOGGER.info(res)


def test_get_pet(get_book_api):
    api = get_book_api
    res = api.get_pet(id="167")
    LOGGER.info(res)



def test_delete_pet(get_book_api):
    api = get_book_api
    res = api.delete_pet(id="167",data=None)
    LOGGER.info(res)


def test_find_by_status(get_book_api):
    api = get_book_api
    res = api.find_by_status(status='available')
    LOGGER.info(res)