import pytest
import random
import allure
from api_source.api.account_api import AccountApi
from commons import utils
from api_source.models.api_user_dto import ApiUserDto
from commons.utils import json_read
from api_source.core import rest
from api_source.api.authors_api import AuthorsApi
from api_source.core.constant import *
from commons.generate_data import RandomData


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


#############################################
###########    INVALID CASES    #############
#############################################
@allure.epic("API")
class TestAPI:

    @pytest.mark.smoke
    @allure.feature("Feature: Register")
    @allure.title("test register valid")
    def test_register(self, get_account_api, generate_new_user):
        api = get_account_api
        user = generate_new_user
        res = api.register(data=user)
        assert res['code'] == 200

    @pytest.mark.smoke
    @allure.feature("Feature: Register")
    @allure.title("Register exists account")
    def test_register_exists_user(self, get_account_api, fix_user):
        api = get_account_api
        user = fix_user
        res = api.register(data=user)
        assert res['code'] == 400 and "DuplicateUserName" in res['msg']

    @pytest.mark.smoke
    @allure.feature("Feature: Login")
    @allure.title("Login user not exists")
    def test_login_user_not_exists(self, get_account_api):
        api = get_account_api
        res = api.login(data={
            "email": "",
            "password": ""
        })

    @pytest.mark.smoke
    @allure.feature("Feature: Login")
    @allure.title("Login valid")
    def test_login(self, get_account_api, fix_user):
        api = get_account_api
        res = api.login(data={"email": "adi@sela.co.il", "password": "string11", })

    @pytest.mark.smoke
    @allure.title("Add author")
    def test_post_authors(self, authors_api):
        author = authors_api.post_authors(data={"name": "test", "homeLatitude": 0, "homeLongitude": 0})
        authors = authors_api.get_authors()
        assert author in authors
        authors_api.delete_author(id=author.id)

    @pytest.mark.smoke
    @allure.title("Delete author")
    def test_delete_author(self, authors_api):
        api = authors_api
        author = api.post_authors(data={"name": "test", "homeLatitude": 0, "homeLongitude": 0})
        res = api.delete_author(id=author.id)
        assert res['code'] is 204
        authors = api.get_authors()
        assert author not in authors

    @pytest.mark.smoke
    @allure.title("Get authors")
    def test_get_authors(self, authors_api):
        api = authors_api
        author = api.post_authors(data={"name": "david", "homeLatitude": 0, "homeLongitude": 0})
        authors = api.get_authors()
        assert author in authors
        api.delete_author(id=author.id)
        authors = api.get_authors()
        assert author not in authors

    @pytest.mark.smoke
    @allure.title("Refresh token")
    def test_refresh_token(self, get_account_api, fix_user):
        api = get_account_api
        res = api.refresh_token(data=fix_user)
