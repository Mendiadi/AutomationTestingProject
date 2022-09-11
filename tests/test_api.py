import logging
from api_source.models.get_author_dto import GetAuthorDto
import pytest
import allure


@allure.epic("API Authentication system")
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
        user = fix_user['user']
        res = api.register(data=user)
        assert res['code'] == 400 and "DuplicateUserName" in res['msg']

    @pytest.mark.smoke
    @allure.feature("Feature: Login")
    @allure.title("Login user not exists")
    def test_login_user_not_exists(self, get_account_api,random_data):
        api = get_account_api
        res = api.login(data={
            "email": random_data.email(),
            "password": random_data.password()
        })
        assert res['code'] == 401 and "Unauthorized" in res['msg']

    @pytest.mark.smoke
    @allure.feature("Feature: Login")
    @allure.title("Login without email")
    def test_login_no_email(self, get_account_api,random_data):
        api = get_account_api
        res = api.login(data={
            "password": random_data.password()
        })
        assert res['code'] == 400 and "The Email field is required" in res['msg']

    @pytest.mark.smoke
    @allure.feature("Feature: Login")
    @allure.title("Login without password")
    def test_login_no_password(self, get_account_api,random_data):
        api = get_account_api
        res = api.login(data={
            "email": random_data.email()
        })
        assert res['code'] == 400 and "The Password field is required" in res['msg']

    @pytest.mark.smoke
    @pytest.mark.parametrize("password,excepted",
                             [(("aaa"),("Your password is limited to 4 to 15 characters" ))
                            ,(("asdfdsasdfdsdfss"),("Your password is limited to 4 to 15 characters"))])
    @allure.feature("Feature: Login")
    @allure.title("Login invalid  password")
    def test_login_invalid_password(self, get_account_api, random_data,excepted,password):
        api = get_account_api
        res = api.login(data={
            "email": random_data.email(),
            "password": password
        })
        assert res['code'] == 400 and excepted in res['msg']


    @pytest.mark.smoke
    @allure.feature("Feature: Login")
    @allure.title("Login valid")
    def test_login(self, get_account_api, fix_user):
        login_user = fix_user['user'].convert_to_login_dto_obj()
        excepted_userid = fix_user['userid']
        api = get_account_api
        user = api.login(data=login_user)
        assert user.userId == excepted_userid


    @pytest.mark.smoke
    @allure.title("Refresh token valid")
    def test_refresh_token(self, get_account_api, fix_user):
        api = get_account_api
        user = fix_user['user'].convert_to_login_dto_obj()
        user_res = api.login(data=user)
        res = api.refresh_token(data=user_res)
        assert res['code'] == 200
        assert res['res'].userId == user_res.userId
        assert res['res'].token != user_res.token

    @pytest.mark.smoke
    @allure.title("Refresh token invalid data")
    def test_refresh_invalid_token(self, get_account_api):
        api = get_account_api
        res = api.refresh_token(data="i")
        assert res['code'] == 400

@allure.epic("Authors testing from api")
class TestAuthors:

    @pytest.mark.smoke
    @allure.title("case Add author")
    def test_post_authors(self, authors_api,create_author_dto_):
        author = authors_api.post_authors(data=create_author_dto_)
        authors = authors_api.get_authors()
        assert author in authors
        authors_api.delete_author(id=author.id)


    @pytest.mark.smoke
    @allure.title("case Delete author")
    def test_delete_author(self, authors_api,create_author_dto_):
        api = authors_api
        author = api.post_authors(data=create_author_dto_)
        res = api.delete_author(id=author.id)
        assert res['code'] is 204
        authors = api.get_authors()
        assert author not in authors

    @pytest.mark.smoke
    @allure.title("case Get authors")
    def test_get_authors(self, authors_api,create_author_dto_):
        api = authors_api
        author = api.post_authors(data=create_author_dto_)
        authors = api.get_authors()
        assert author in authors
        api.delete_author(id=author.id)
        authors = api.get_authors()
        assert author not in authors

    @allure.title("case get by id")
    def test_author_by_id(self,authors_api,create_author_dto_):
        api = authors_api
        author = api.post_authors(data=create_author_dto_)
        author2 = api.get_author_by_id(id=author.id)
        assert author2 == author
        api.delete_author(id=author.id)

    @allure.title("case put by id")
    def test_put_author_by_id(self, authors_api,create_author_dto_):
        api = authors_api
        author = api.post_authors(data=create_author_dto_)
        author.name = "eyal"
        author_obj = GetAuthorDto.create_from_author(author)
        api.put_author_by_id(data=author_obj, id=author.id)
        assert author.name == "eyal"
        api.delete_author(id=author.id)


    @allure.title("search by query and by substring")
    def test_search(self,authors_api,create_author_dto_):
        api = authors_api
        a = create_author_dto_
        api.post_authors(data=a)
        authors = api.search(query="moshe")
        assert [a.name == "moshe" or a.name.find("moshe") >= 1 for a in authors]




def test_delete_all_authors(authors_api):

    api = authors_api
    authors = api.get_authors()
    if len(authors) < 50:
        pytest.skip(reason="not too many moshes")

    for author in authors:
        if author.id > 3:
            res = api.delete_author(id=author.id)
    a = api.get_authors()