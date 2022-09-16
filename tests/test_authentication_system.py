import time
import logging
import pytest
import allure

LOGGER = logging.getLogger(__name__)


@allure.epic("API Authentication system")
class TestAuthenticationAPI:

    @allure.feature("Feature: Register")
    @allure.title("test register valid")
    def test_register(self, api, random_data):
        user = random_data.generate_account()
        res = api.account.register(user)
        assert res['code'] == 200

    def test_register_invalid_data(self):
        pass


    def test_login_invalid_email(self):
        pass

    @allure.feature("Feature: Register")
    @allure.title("Register exists account")
    def test_register_exists_user(self, api, fix_user):
        user = fix_user['user']
        res = api.account.register(user)
        assert res['code'] == 400 and "DuplicateUserName" in res['msg']

    @allure.feature("Feature: Login")
    @allure.title("Login user not exists")
    def test_login_user_not_exists(self, api, random_data):
        res = api.account.login({
            "email": random_data.email(),
            "password": random_data.password()
        })
        assert res['code'] == 401 and "Unauthorized" in res['msg']

    @allure.feature("Feature: Login")
    @allure.title("Login without email")
    def test_login_no_email(self, api, random_data):
        res = api.account.login({
            "password": random_data.password()
        })
        assert res['code'] == 400 and "The Email field is required" in res['msg']

    @allure.feature("Feature: Login")
    @allure.title("Login without password")
    def test_login_no_password(self, api, random_data):
        res = api.account.login({
            "email": random_data.email()
        })
        assert res['code'] == 400 and "The Password field is required" in res['msg']

    @pytest.mark.parametrize("password,excepted",
                             [("aaa", "Your password is limited to 4 to 15 characters")
                                 , ("asdfdsasdfdsdfss", "Your password is limited to 4 to 15 characters")])
    @allure.feature("Feature: Login")
    @allure.title("Login invalid  password")
    def test_login_invalid_password(self, api, random_data, excepted, password):
        res = api.account.login({
            "email": random_data.email(),
            "password": password
        })
        assert res['code'] == 400 and excepted in res['msg']

    @allure.feature("Feature: Login")
    @allure.title("Login valid")
    def test_login(self, api, fix_user):
        login_user = fix_user['user'].convert_to_login_dto_obj()
        excepted_userid = fix_user['userid']
        user = api.account.login(login_user)
        assert user.token is not None

    @allure.title("Refresh token valid")
    def test_refresh_token(self, api, fix_user):
        user = fix_user['user'].convert_to_login_dto_obj()
        user_res = api.account.login(user)
        res = api.account.refresh_token(user_res)
        assert res['code'] == 200
        assert res['res'].userId == user_res.userId
        assert res['res'].token != user_res.token

    @allure.title("Refresh token invalid data")
    def test_refresh_invalid_token(self,api):
        res = api.account.refresh_token("i")
        assert res['code'] == 400


@allure.epic("UI Authentication system")
class TestAuthenticationUI:

    def test_logout(self):
        pytest.skip()
        pass

    @pytest.mark.regression
    @allure.feature("Feature: Login")
    @allure.title("verify Login")
    def test_login(self, get_main_page, get_test_data):
        LOGGER.info("login valid")
        store_page = get_main_page.login(get_test_data.email, get_test_data.password)
        time.sleep(5)
        text = store_page.get_label_h1_text()
        LOGGER.info(text)
        assert text == 'Welcome to our store'

    def test_login_invalid_cases(self):
        pytest.skip()
        pass

    def test_register_invalid_cases(self):
        pytest.skip()
        pass

    def test_register_exists(self):
        pytest.skip()
        pass

    def test_register_and_login(self):
        pytest.skip()
        pass

    @allure.feature("Feature: Register")
    @allure.title("verify register")
    def test_register(self, get_main_page, random_data):
        register_page = get_main_page.click_register()
        register_page.register(random_data.email(), random_data.password(), random_data.firstname(),
                               random_data.lastname())
