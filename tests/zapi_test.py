import logging
from api_source.models.get_author_dto import GetAuthorDto
import pytest
import allure


@allure.epic("Authors testing from api")
class TestAuthors:

    @pytest.mark.regression
    @allure.title("case Add author")
    def test_post_authors(self, authors_api, random_data):
        author = authors_api.post_authors(random_data.generate_author())
        authors = authors_api.get_authors()
        assert author in authors

    @pytest.mark.smoke
    @allure.title("case Delete author")
    def test_delete_author(self, authors_api, random_data):
        api = authors_api
        author = api.post_authors(random_data.generate_author())
        res = api.delete_author(id=author.id)
        assert res['code'] is 204
        authors = api.get_authors()
        assert author not in authors

    @pytest.mark.smoke
    @allure.title("case Get authors")
    def test_get_authors(self, authors_api, random_data):
        api = authors_api
        author = api.post_authors(random_data.generate_author())
        authors_api.delete_author(id=17)
        authors = api.get_authors()
        assert author in authors
        api.delete_author(id=author.id)
        authors = api.get_authors()
        assert author not in authors

    @allure.title("case get by id")
    def test_author_by_id(self, authors_api, random_data):
        api = authors_api
        author = api.post_authors(random_data.generate_author())
        author2 = api.get_author_by_id(id=author.id)
        assert author2 == author

    @allure.title("case put by id")
    def test_put_author_by_id(self, authors_api, random_data):
        api = authors_api
        author = api.post_authors(random_data.generate_author())
        author.name = "eyal"
        author_obj = GetAuthorDto.create_from_author(author)
        api.put_author_by_id(author_obj, id=author.id)
        assert author.name == "eyal"

    @pytest.mark.parametrize("query", ["m", "at", "geroge", "l"])
    @allure.title("case valid search given true results")
    def test_search(self, authors_api, query):
        api = authors_api
        authors_get = api.get_authors()
        authors = api.search(query=query)
        if len(authors) > 0:
            assert [author.name == query or query in author.name for author in authors]
        else:
            assert [query not in author.name for author in authors_get]


def test_delete_all_authors(authors_api):
    api = authors_api
    authors = api.get_authors()
    if len(authors) < 50:
        pytest.skip(reason="not too many moshes")
    for author in authors:
        if author.id > 3:
            api.delete_author(id=author.id)


@allure.epic("books from api")
class TestBook:

    @allure.title("get book by id")
    def test_get_book_by_id_valid(self, book_api, random_data, authors_api):
        author_create = random_data.generate_author(name="sami")
        author = authors_api.post_authors(author_create)
        book_create = random_data.generate_book(name="my sami book", authorid=author.id)
        book = book_api.post_books(book_create)
        get_book = book_api.get_book_by_id(id=book.id)
        book = book.convert_to_book_dto()
        assert get_book == book
        authors_api.delete_author(id=author.id)
        assert book_api.get_book_by_id(id=book.id)['code'] == 404

    @pytest.mark.parametrize("id,excepted,code",
                             [((-7), ("Not Found"), (404)), (("df"), ("The value \'df\' is not valid"), (400))])
    @allure.title("get book by id invalid")
    def test_get_book_by_id_invalid(self, book_api, id, excepted, code):
        api = book_api
        res = api.get_book_by_id(id=id)
        assert res['code'] == code
        assert excepted in res['msg']

    @allure.title("get books")
    def test_get_books(self, book_api, random_data, authors_api):
        author_create = random_data.generate_author("mr sami")
        author = authors_api.post_authors(author_create)
        api = book_api
        book_dto = random_data.generate_book(authorid=author.id)
        book = api.post_books(book_dto)
        books = api.get_books()
        assert book.convert_to_book_dto() in books

    @allure.title("case delete book normal user")
    def test_delete_book_normal_user(self, book_api, random_data, authors_api):
        author_dto = random_data.generate_author()
        author = authors_api.post_authors(author_dto)
        author = authors_api.get_author_by_id(id=author.id)
        book_dto = random_data.generate_book(authorid=author.id, name="shay")
        book = book_api.post_books(book_dto)
        books = book_api.get_books()
        book = book.convert_to_book_dto()
        assert book in books
        book_api.delete_book(id=book.id)
        books = book_api.get_books()
        assert book in books

    @allure.title("case delete book invalid id")
    def test_delete_book_invalid_id(self, book_api, random_data, authors_api):
        res = book_api.delete_book(id="sds")
        assert res['code'] > 200

    @allure.title("case post book invalid data")
    def test_post_book_invalid_data(self, book_api):
        res = book_api.post_books("{moshe:123,tamir:adi}")
        assert res['code'] == 400
        assert 'The JSON value could not be converted' in res['msg']

    @allure.title("try to post book with invalid id ")
    @pytest.mark.parametrize("id,excepted", [((-1), ("The field AuthorId must be between 1 and 2147483647.")),
                                             ((2147483647), ("The field AuthorId must be between 1 and 2147483647."))
        , (("sfsf"), ("The JSON value could not be converted to System.Int32."))])
    def test_post_book_invalid_id(self, id, excepted, random_data, book_api):
        book_dto = random_data.generate_book(authorid=id)
        book = book_api.post_books(book_dto)
        assert book['code'] == 400
        assert excepted in book['msg']

    @pytest.mark.parametrize("name,excepted", [((2), ("The JSON value could not be converted to System.String."))
        , ((None), ("The JSON value could not be converted to System.String."))])
    def test_post_book_no_name(self, random_data, book_api, name, excepted):
        book_dto = random_data.generate_book(name=3)
        book = book_api.post_books(book_dto)
        assert excepted in book['msg'] and book['code'] == 400

    def test_post_book_invalid_author(self):
        pass

    @allure.title("case post books")
    def test_post_book(self, book_api, random_data, authors_api):
        new_author = random_data.generate_author()
        author = authors_api.post_authors(new_author)
        new_book = random_data.generate_book(authorid=author.id)
        book = book_api.post_books(new_book)
        books = book_api.get_books()
        author = authors_api.get_author_by_id(id=author.id)
        logging.info(f"book - ,{author},{author.books}")
        assert [book.id == b.id for b in books]
        assert [book.id == b['id'] for b in author.books]
        logging.info(f"book - {books},{author},{author.books}")

    @allure.title("case delete book admin user")
    def test_delete_book_from_admin(self, fix_admin_user, book_api, authors_api, get_account_api, random_data):
        author_dto = random_data.generate_author()
        author = authors_api.post_authors(author_dto)
        author = authors_api.get_author_by_id(id=author.id)
        book_dto = random_data.generate_book(authorid=author.id, name="shay")
        book = book_api.post_books(book_dto)
        res = get_account_api.login(fix_admin_user)
        book_api.session.update_token(res.token)
        book_api.delete_book(id=book.id)
        books = book_api.get_books()
        assert book not in books


class TestAPISUnauthorized:

    def test_unauthorized_delete_book(self, book_api):
        book_api.session.headers.clear()
        res = book_api.delete_book(id=5)
        assert res['code'] == 401

    def test_unauthorized_post_book(self, book_api, random_data):
        book = random_data.generate_book(authorid=2)
        res = book_api.post_books(book)
        assert res['code'] == 401

    def test_unauthorized_post_author(self, authors_api, random_data):
        author = random_data.generate_author()
        res = authors_api.post_authors(author)
        assert res['code'] == 401

    def test_unauthorized_put_author(self, authors_api, random_data):
        author = random_data.generate_author()
        res = authors_api.put_author_by_id(author, id=4)
        assert res['code'] == 401

    def test_unauthorized_delete_author(self, authors_api, get_account_api, fix_user):
        res = authors_api.delete_author(id=5)
        response = get_account_api.login(fix_user['user'])
        authors_api.session.update_token(response.token)
        assert res['code'] == 401
