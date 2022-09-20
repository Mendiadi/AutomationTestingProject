import allure
import pytest
from commons.utils import log_name

@allure.epic("verify search page works properly")
class TestSearchPage:

    @log_name
    @allure.title("case search with no query gives all result")
    def test_search_empty_query(self, book_setup, author_setup, api, main_page):
        search_page = main_page.search("")
        search_page.reload()
        assert len(search_page.get_books()) == len(api.books.get_books())
        assert len(search_page.get_authors()) == len(api.authors.get_authors())

    @log_name
    @allure.title("case search query gives also substring cases")
    def test_search_and_also_sub_string_apear(self, api, data, main_page):
        author = api.authors.post_authors(data.generate_author(name="oren"))
        api.books.post_books(data.generate_book(authorid=author.id, name="oren domi"))
        search_page = main_page.search("or")
        search_page.reload()
        books, authors = search_page.get_books(), search_page.get_authors()
        books_name = [search_page.get_book_title(book_) for book_ in books]
        assert "oren domi" in books_name
        for b_name in books_name:
            assert "or" in b_name


    def test_search_for_book(self):
        pytest.skip("not implemented")
        ...
