import logging
from api_source.models.get_author_dto import GetAuthorDto
import pytest
import allure






@allure.epic("Authors testing from api")
class TestAuthors:

    @pytest.mark.smoke
    @allure.title("case Add author")
    def test_post_authors(self, authors_api, random_data):
        author = authors_api.post_authors(random_data.generate_author())
        authors = authors_api.get_authors()
        assert author in authors
        authors_api.delete_author(id=author.id)

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
        api.delete_author(id=author.id)

    @allure.title("case put by id")
    def test_put_author_by_id(self, authors_api, random_data):
        api = authors_api
        author = api.post_authors(random_data.generate_author())
        author.name = "eyal"
        author_obj = GetAuthorDto.create_from_author(author)
        api.put_author_by_id(author_obj, id=author.id)
        assert author.name == "eyal"
        api.delete_author(id=author.id)

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


@allure.epic("books from api")
class TestBook:

    @allure.title("get books")
    def test_get_books(self, book_api, random_data):
        api = book_api
        book = random_data.generate_book()
        books = api.get_books()

    @allure.title("case delete book")
    def test_delete_book(self, book_api, random_data, authors_api):
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
        assert book not in books

    @allure.title("case delete book invalid id")
    def test_delete_book_invalid_id(self, book_api, random_data, authors_api):
        res = book_api.delete_book(id="sds")
        assert res['code'] > 200

    @allure.title("case post book invalid data")
    def test_post_book_invalid_data(self, book_api):
        res = book_api.post_books("{moshe:123,tamir:adi}")
        assert res['code'] == 400
        assert 'The JSON value could not be converted' in res['msg']

    def test_post_book_invalid_id(self):
        pass

    def test_post_book_no_name(self):
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
        authors_api.delete_author(id=author.id)


def test_delete_all_authors(authors_api):
    api = authors_api
    authors = api.get_authors()
    if len(authors) < 50:
        pytest.skip(reason="not too many moshes")
    for author in authors:
        if author.id > 3:
            api.delete_author(id=author.id)
