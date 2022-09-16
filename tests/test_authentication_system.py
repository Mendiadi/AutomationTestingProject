import pytest
import allure
from commons.utils import log_name



@allure.epic("API Authentication system")
class TestAuthenticationAPI:
    @log_name
    @allure.feature("Feature: Register")
    @allure.title("test register valid")
    def test_register(self, api, data):
        user = data.generate_account()
        res = api.account.register(user)
        assert res['code'] == 200

    @log_name
    def test_register_invalid_data(self):
        pass

    @log_name
    def test_login_invalid_email(self):
        pass

    @log_name
    @allure.feature("Feature: Register")
    @allure.title("Register exists account")
    def test_register_exists_user(self, api, fix_user):
        user = fix_user['user']
        res = api.account.register(user)
        assert res['code'] == 400 and "DuplicateUserName" in res['msg']

    @log_name
    @allure.feature("Feature: Login")
    @allure.title("Login user not exists")
    def test_login_user_not_exists(self, api, data):
        res = api.account.login({
            "email": data.email(),
            "password": data.password()
        })
        assert res['code'] == 401 and "Unauthorized" in res['msg']

    @log_name
    @allure.feature("Feature: Login")
    @allure.title("Login without email")
    def test_login_no_email(self, api, data):
        res = api.account.login({
            "password": data.password()
        })
        assert res['code'] == 400 and "The Email field is required" in res['msg']

    @log_name
    @allure.feature("Feature: Login")
    @allure.title("Login without password")
    def test_login_no_password(self, api, data):
        res = api.account.login({
            "email": data.email()
        })
        assert res['code'] == 400 and "The Password field is required" in res['msg']

    @log_name
    @pytest.mark.parametrize("password,excepted",
                             [("aaa", "Your password is limited to 4 to 15 characters")
                                 , ("asdfdsasdfdsdfss", "Your password is limited to 4 to 15 characters")])
    @allure.feature("Feature: Login")
    @allure.title("Login invalid  password")
    def test_login_invalid_password(self, api, data, excepted, password):
        res = api.account.login({
            "email": data.email(),
            "password": password
        })
        assert res['code'] == 400 and excepted in res['msg']

    @log_name
    @allure.feature("Feature: Login")
    @allure.title("Login valid")
    def test_login(self, api, fix_user):
        login_user = fix_user['user'].convert_to_login_dto_obj()
        excepted_userid = fix_user['userid']
        user = api.account.login(login_user)
        assert user.token is not None

    @log_name
    @allure.title("Refresh token valid")
    def test_refresh_token(self, api, fix_user):
        user = fix_user['user'].convert_to_login_dto_obj()
        user_res = api.account.login(user)
        res = api.account.refresh_token(user_res)
        assert res['code'] == 200
        assert res['res'].userId == user_res.userId
        assert res['res'].token != user_res.token

    @log_name
    @allure.title("Refresh token invalid data")
    def test_refresh_invalid_token(self, api):
        res = api.account.refresh_token("i")
        assert res['code'] == 400


@allure.epic("UI Authentication system")
class TestAuthenticationUI:
    @log_name
    def test_logout(self):
        pytest.skip()
        pass

    @log_name
    @pytest.mark.regression
    @allure.feature("Feature: Login")
    @allure.title("verify Login valid")
    def test_login_valid(self, main_page, get_test_data):
        store_page = main_page.login(get_test_data.email, get_test_data.password)
        text = store_page.get_label_h1_text()
        assert text == 'Welcome to our store'

    @log_name
    def test_login_invalid_cases(self):
        pytest.skip()
        pass

    @log_name
    def test_register_invalid_cases(self):
        pytest.skip()
        pass

    @log_name
    def test_register_exists(self):
        pytest.skip()
        pass

    @log_name
    def test_register_and_login(self):
        pytest.skip()
        pass

    @log_name
    @allure.feature("Feature: Register")
    @allure.title("verify register")
    def test_register(self, main_page, data):
        register_page = main_page.click_register()
        register_page.register(data.email(), data.password(), data.firstname(),
                               data.lastname())
