import pytest
import allure
from core.models import GetAuthorDto
from commons.utils import log_name


@allure.epic("Authors testing from api")
class TestAuthors:

    def test_post_author_invalid_data(self):
        pytest.skip()
        pass

    def test_put_author_invalid_data(self):
        pytest.skip()
        pass

    @log_name
    @pytest.mark.regression
    @allure.title("case Add author")
    def test_post_authors(self, api, data):
        author = api.authors.post_authors(data.generate_author())
        authors = api.authors.get_authors()
        assert author in authors
        api.authors.delete_author(id=author.id)

    def test_delete_author_by_id_invalid(self):
        pass

    @log_name
    @pytest.mark.smoke
    @allure.title("case Delete author")
    def test_delete_author(self, api, data):
        author = api.authors.post_authors(data.generate_author())
        res = api.authors.delete_author(id=author.id)
        assert res['code'] is 204
        authors = api.authors.get_authors()
        assert author not in authors

    @log_name
    @pytest.mark.smoke
    @allure.title("case Get authors")
    def test_get_authors(self, api, data):
        author = api.authors.post_authors(data.generate_author())
        api.authors.delete_author(id=17)
        authors = api.authors.get_authors()
        assert author in authors
        api.authors.delete_author(id=author.id)
        authors = api.authors.get_authors()
        assert author not in authors

    @log_name
    @allure.title("case get by id")
    def test_author_by_id(self, api, data):
        author = api.authors.post_authors(data.generate_author())
        author2 = api.authors.get_author_by_id(id=author.id)
        assert author2 == author

    @log_name
    @allure.title("case put by id")
    def test_put_author_by_id(self, api, data):
        author = api.authors.post_authors(data.generate_author())
        author.name = "eyal"
        author_obj = GetAuthorDto.create_from_author(author)
        api.authors.put_author_by_id(author_obj, id=author.id)
        assert author.name == "eyal"

    @log_name
    @pytest.mark.parametrize("query", ["m", "at", "geroge", "l"])
    @allure.title("case valid search given true results")
    def test_search(self, api, query):
        authors_get = api.authors.get_authors()
        authors = api.authors.search(query=query)
        if len(authors) > 0:
            assert [author.name == query or query in author.name for author in authors]
        else:
            assert [query not in author.name for author in authors_get]


@allure.epic("books from api")
class TestBook:

    @log_name
    @allure.title("get book by id")
    def test_get_book_by_id_valid(self, api, data):
        author_create = data.generate_author(name="sami")
        author = api.authors.post_authors(author_create)
        book_create = data.generate_book(name="my sami book", authorid=author.id)
        book = api.books.post_books(book_create)
        get_book = api.books.get_book_by_id(id=book.id)
        book = book.convert_to_book_dto()
        assert get_book == book
        api.authors.delete_author(id=author.id)
        assert api.books.get_book_by_id(id=book.id)['code'] == 404

    @log_name
    @pytest.mark.parametrize("id,excepted,code",
                             [((-7), "Not Found", 404), ("df", "The value \'df\' is not valid", 400)])
    @allure.title("get book by id invalid")
    def test_get_book_by_id_invalid(self, api, id, excepted, code):
        res = api.books.get_book_by_id(id=id)
        assert res['code'] == code
        assert excepted in res['msg']

    @log_name
    @allure.title("get books")
    def test_get_books(self, api, data):
        author_create = data.generate_author("mr sami")
        author = api.authors.post_authors(author_create)
        book_dto = data.generate_book(authorid=author.id)
        book = api.books.post_books(book_dto)
        books = api.books.get_books()
        assert book.convert_to_book_dto() in books
        api.authors.delete_author(id=author.id)

    @log_name
    @allure.title("case delete book normal user")
    def test_delete_book_normal_user(self, api, data):
        author_dto = data.generate_author()
        author = api.authors.post_authors(author_dto)
        author = api.authors.get_author_by_id(id=author.id)
        book_dto = data.generate_book(authorid=author.id, name="shay")
        book = api.books.post_books(book_dto)
        books = api.books.get_books()
        book = book.convert_to_book_dto()
        assert book in books
        api.books.delete_book(id=book.id)
        books = api.books.get_books()
        assert book in books
        api.authors.delete_author(id=author.id)

    @log_name
    @allure.title("case delete book invalid id")
    def test_delete_book_invalid_id(self, api, data):
        res = api.books.delete_book(id="sds")
        assert res['code'] > 200

    @log_name
    @allure.title("case post book invalid data")
    def test_post_book_invalid_data(self, api):
        res = api.books.post_books("{moshe:123,tamir:adi}")
        assert res['code'] == 400
        assert 'The JSON value could not be converted' in res['msg']

    @log_name
    @allure.title("try to post book with invalid id ")
    @pytest.mark.parametrize("id,excepted", [((-1), "The field AuthorId must be between 1 and 2147483647."),
                                             (2147483648, "The field AuthorId must be between 1 and 2147483647.")
        , ("sfsf", "The JSON value could not be converted to System.Int32.")])
    def test_post_book_invalid_id(self, id, excepted, data, api):
        book_dto = data.generate_book(authorid=id)
        book = api.books.post_books(book_dto)
        assert book['code'] == 400
        assert excepted in book['msg']

    @log_name
    @pytest.mark.parametrize("name,excepted", [(2, "The JSON value could not be converted to System.String.")
        , (None, "The JSON value could not be converted to System.String.")])
    def test_post_book_no_name(self, data, api, name, excepted):
        book_dto = data.generate_book(name=3)
        book = api.books.post_books(book_dto)
        assert excepted in book['msg'] and book['code'] == 400

    @log_name
    @allure.title("case post book with no exists author id")
    def test_post_book_no_exists_author(self, api, data):
        api.authors.delete_author(id=100)
        res = api.books.post_books(data.generate_book(authorid=100))
        assert res['code'] == 400

    @log_name
    @allure.title("case post books")
    def test_post_book(self, api, data):
        new_author = data.generate_author()
        author = api.authors.post_authors(new_author)
        new_book = data.generate_book(authorid=author.id)
        book = api.books.post_books(new_book)
        books = api.books.get_books()
        author = api.authors.get_author_by_id(id=author.id)
        assert [book.id == b.id for b in books]
        assert [book.id == b['id'] for b in author.books]
        api.authors.delete_author(id=author.id)

    @log_name
    @allure.title("case put update book")
    def test_put_book(self, api, data):
        new_author = data.generate_author()
        author = api.authors.post_authors(new_author)
        new_book = data.generate_book(authorid=author.id)
        book = api.books.post_books(new_book)
        book.name = "adi hagever"
        book.amountInStock = 5
        api.books.put_book(book, id=book.id)
        same_book = api.books.get_book_by_id(id=book.id)
        assert same_book.name == "adi hagever" and same_book.amountInStock == 5
        api.authors.delete_author(id=author.id)

    @log_name
    @allure.title("case put book invalid id")
    @pytest.mark.parametrize("id,excepted", [(10, 400), (-20, 400), ("ss", 400)])
    def test_put_book_invalid_id(self, api, data, id, excepted):
        new_author = data.generate_author()
        author = api.authors.post_authors(new_author)
        new_book = data.generate_book(authorid=author.id)
        book = api.books.post_books(new_book)
        res = api.books.put_book(book, id=id)
        assert res['code'] == excepted
        api.authors.delete_author(id=author.id)

    @log_name
    @allure.title("case put book invalid data")
    def test_put_book_invalid_data(self, api):
        res = api.books.put_book({}, id=4)
        assert res['code'] == 400

    @log_name
    @allure.title("case delete book admin user")
    def test_delete_book_from_admin(self, fix_admin_user, api, data):
        author_dto = data.generate_author()
        author = api.authors.post_authors(author_dto)
        author = api.authors.get_author_by_id(id=author.id)
        book_dto = data.generate_book(authorid=author.id, name="shay")
        book = api.books.post_books(book_dto)
        res = api.account.login(fix_admin_user)
        api.session.update_token(res.token)
        api.books.delete_book(id=book.id)
        books = api.books.get_books()
        assert book not in books
        api.authors.delete_author(id=author.id)

    def test_purchase_book(self):
        pass

    def test_purchase_book_invalid(self):
        pass

    def test_find_book_by_author(self):
        pass

    @allure.title("")
    def find_book_by_author_invalid(self):
        pass


@allure.epic("API verify authorized required")
class TestAPISUnauthorized:

    @log_name
    @allure.title("case delete book")
    def test_unauthorized_delete_book(self, api):
        api.session.headers.clear()
        res = api.books.delete_book(id=5)
        assert res['code'] == 401
        assert res['reason'] == "Unauthorized"

    @log_name
    @allure.title("case post book")
    def test_unauthorized_post_book(self, api, data):
        book = data.generate_book(authorid=2)
        res = api.books.post_books(book)
        assert res['code'] == 401
        assert res['reason'] == "Unauthorized"

    @log_name
    @allure.title("case put book")
    def test_put_book_unauthorized(self, api):
        res = api.books.put_book({}, id=10)
        assert res['code'] == 401
        assert res['reason'] == "Unauthorized"

    @log_name
    @allure.title("case post author")
    def test_unauthorized_post_author(self, api, data):
        author = data.generate_author()
        res = api.authors.post_authors(author)
        assert res['code'] == 401
        assert res['reason'] == "Unauthorized"

    @log_name
    @allure.title("case put author")
    def test_unauthorized_put_author(self, api, data):
        author = data.generate_author()
        res = api.authors.put_author_by_id(author, id=4)
        assert res['code'] == 401
        assert res['reason'] == "Unauthorized"

    @log_name
    @allure.title("case purchase book")
    def test_unauthorized_purchase_book(self, data, api):
        res = api.books.purchase_book(id=3)
        assert res['code'] == 401
        assert res['reason'] == "Unauthorized"

    @log_name
    @allure.title("case delete author")
    def test_unauthorized_delete_author(self, api, fix_user):
        res = api.authors.delete_author(id=5)
        response = api.account.login(fix_user['user'])
        api.session.update_token(response.token)
        assert res['code'] == 401
        assert res['reason'] == "Unauthorized"
