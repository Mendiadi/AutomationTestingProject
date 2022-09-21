import pytest
import allure
from commons.utils import log_name

register__all_invalid_msg = 'Email":["The Email field is required."],"LastName":["The LastName field is required."]' \
                            ',"Password":["The Password field is required."],"FirstName":["The FirstName field is required."'
register_password_msg = "The Password field is required."
register_email_msg = "The Email field is required."
register_first_name_msg = "The FirstName field is required."
register_last_name_msg = "The LastName field is required."
register_password_len__msg = "Your password is limited to 4 to 15 characters"
register_email_not_valid_msg = "The Email field is not a valid e-mail address."


@pytest.mark.usefixtures("safe_load")
@allure.epic("API Authentication system")
class TestAuthenticationAPI:
    @log_name
    @allure.feature("Feature: Register")
    @allure.title("test register valid")
    def test_register(self, api, data):
        user = data.generate_account()
        res = api.account.register(user)
        assert res['code'] == 200
        after_res = api.account.register(user)
        assert after_res['code'] == 400
        assert f"Username \'{user.email}\' is already taken." in after_res['msg']

    @log_name
    @allure.feature("Feature: Register")
    @allure.title("case register from api with invalid data")
    @pytest.mark.parametrize("data_,expected", [({}, register__all_invalid_msg),
                                                ({"email": "", "password": "12345", "firstname": "string",
                                                  "lastname": "string"}, register_email_msg),
                                                ({"email": "aa@aa.cm", "password": "12345", "firstname": "string",
                                                  "lastname": ""}, register_last_name_msg),
                                                ({"email": "aa@aa.cm", "password": "12345", "firstname": "",
                                                  "lastname": "string"}, register_first_name_msg),
                                                ({"email": "aa@aa.cm", "password": "", "firstname": "string",
                                                  "lastname": "string"}, register_password_msg),
                                                ({"email": "aa@aa.cm", "password": "123", "firstname": "string",
                                                  "lastname": "string"}, register_password_len__msg),
                                                ({"email": "aa@aa.cm", "password": "1266776544563666",
                                                  "firstname": "string", "lastname": "string"},
                                                 register_password_len__msg),
                                                ({"email": "aaaa.cm", "password": "126677", "firstname": "string",
                                                  "lastname": "string"}, register_email_not_valid_msg)])
    def test_register_invalid_data(self, api, expected, data_):
        res = api.account.register(data_)
        assert res['code'] == 400
        assert expected in res['msg']

    @log_name
    @allure.feature("Feature: Login")
    @allure.title("case login from api with invalid email")
    def test_login_invalid_email(self, api):
        res = api.account.login({"email": "wrong-email", "password": "123456"})
        assert res['code'] == 400
        assert "The Email field is not a valid e-mail address." in res['msg']

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
        assert user.userId == excepted_userid
        assert user.token is not None

    @log_name
    @allure.feature("Feature: Login")
    @allure.title("Refresh token valid")
    def test_refresh_token(self, api, fix_user):
        user = fix_user['user'].convert_to_login_dto_obj()
        user_res = api.account.login(user)
        res = api.account.refresh_token(user_res)
        assert res['code'] == 200
        # assert res['res'].userId == user_res.userId
        assert res['res'].token != user_res.token

    @log_name
    @allure.feature("Feature: Login")
    @allure.title("Refresh token invalid data")
    def test_refresh_invalid_token(self, api):
        res = api.account.refresh_token("i")
        assert res['code'] == 400


@allure.epic("UI Authentication system")
class TestAuthenticationUI:
    @log_name
    @allure.feature("Feature: Login")
    @allure.title("case logout")
    def test_logout(self, main_page, configuration, book_setup):
        store_page = main_page.login(configuration.email, configuration.password)
        assert store_page.get_logout_btn_text() == "Log Out"
        store_page.click_logout()
        assert store_page.get_login_btn_text() == "Log In"
        store_page = main_page.click_bookstore()
        books = store_page.get_books()
        msg = store_page.purchase(books[0])
        assert "Must be signed in to purchase." in msg

    @log_name
    @pytest.mark.regression
    @allure.feature("Feature: Login")
    @allure.title("verify Login valid")
    def test_login_valid(self, main_page, configuration):
        store_page = main_page.login(configuration.email, configuration.password)
        text = store_page.get_label_h1_text()
        assert text == 'Welcome to our store'
        assert store_page.get_logout_btn_text() == "Log Out"


    @log_name
    @allure.title("case login from ui invalid ")
    @pytest.mark.parametrize("email,password", [("", "12345"), ("aaaaa@aa", "")])
    @allure.feature("Feature: Login")
    def test_login_invalid_cases(self, email, password, main_page):
        main_page.login(email, password)
        assert main_page.url == "http://localhost/"
        assert main_page.get_login_btn_text() == "Log In"

    @log_name
    def test_register_invalid_cases(self):
        pytest.skip("not implemented")

    @log_name
    def test_register_exists(self):
        pytest.skip("not implemented")

    @log_name
    @allure.feature("Feature: Register")
    @allure.title("verify register")
    def test_register(self, main_page, data, api):
        email = data.email()
        password = data.password()
        register_page = main_page.click_register()
        register_page.register(email, password, data.firstname(),
                               data.lastname())
        login_page = register_page.click_back_login()
        store_page = login_page.login(email, password)
        assert api.account.login({"email": email, "password": password})['code'] == 200
        assert store_page.get_logout_btn_text() == "Log Out"
