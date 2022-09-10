import pytest
import allure


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
