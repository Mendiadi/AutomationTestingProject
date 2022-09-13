import logging
import time
import allure

LOGGER = logging.getLogger(__name__)


@allure.epic("UI store page")
class TestStore:

    @allure.title("get book by title")
    def test_get_book(self, get_main_page):
        store_page = get_main_page.click_bookstore()
        time.sleep(3)
        book = store_page.get_book(title="1984")
        time.sleep(3)
        book_title = store_page.get_book_title(book)
        book_author = store_page.get_book_author(book)
        LOGGER.info(f"title: {book_title} author: {book_author}")
        assert "George Orwell" in book_author

    @allure.title("case buy book without login")
    def test_buy_no_login_book(self, get_main_page, book_api, random_data, authors_api):
        author_created = random_data.generate_author()
        author = authors_api.post_authors(author_created)
        book_created = random_data.generate_book(authorid=author.id, name="shay")
        book = book_api.post_books(book_created)
        store_page = get_main_page.click_bookstore()
        time.sleep(1)
        store_page.reload()
        book1 = store_page.get_book(title=book_created.name)
        LOGGER.info(book1)
        time.sleep(1)
        msg = store_page.purchase(book1)
        LOGGER.info(msg)
        assert book.amountInStock == book_api.get_book_by_id(id=book.id).amountInStock
        assert "Must be signed in to purchase." in msg

    @allure.title("get books by author")
    def test_get_books_by_author(self, get_main_page):
        store_page = get_main_page.click_bookstore()
        time.sleep(3)
        books = store_page.get_books_by_author("George Orwell")
        for book in books:
            book_title = store_page.get_book_title(book)
            LOGGER.info(book_title)
            assert book_title == "1984" or "Animal Farm"

    @allure.title("case buy book with login and created book")
    def test_case_buy_book(self,get_main_page,book_api,random_data,authors_api,get_test_data):
        get_main_page.login(get_test_data.email,get_test_data.password).click_bookstore()
        author_created = random_data.generate_author()
        author = authors_api.post_authors(author_created)
        book_created = random_data.generate_book(authorid=author.id)
        book = book_api.post_books(book_created)
        store_page = get_main_page.click_bookstore()
        time.sleep(1)
        store_page.reload()
        book1 = store_page.get_book(title=book_created.name)
        LOGGER.info(book1)
        time.sleep(1)
        msg = store_page.purchase(book1)
        time.sleep(1)
        store_page.reload()
        amount_in_stock_api = book_api.get_book_by_id(id=book.id).amountInStock
        LOGGER.info(amount_in_stock_api)
        assert book.amountInStock - 1  == amount_in_stock_api
        assert f"Thank you for your purchase of {book.name}" in msg
        authors_api.delete_author(id=author.id)

    @allure.title("case post books and see if they apear at screen")
    def test_books_updated(self, get_main_page, book_api, random_data, authors_api):
        author_new = random_data.generate_author("moshe")

        author = authors_api.post_authors(author_new)
        book_created = random_data.generate_book(name="moshe is hot", authorid=author.id)
        book_api.post_books(book_created)
        store_page = get_main_page.click_bookstore()
        books = store_page.get_books_by_author("moshe")
        for book in books:
            text = store_page.get_book_title(book)
            assert "moshe is hot" == text


    @allure.title("check if all the books in db are visible")
    def test_verify_books(self, get_main_page, book_api):
        boos_api = book_api.get_books()
        store_page = get_main_page.click_bookstore()
        books = store_page.get_books()
        LOGGER.info(books)
        LOGGER.info(boos_api)
        result_book_ui = [store_page.get_book_title(book) for book in books]
        result = [book.name for book in boos_api]
        assert len(result_book_ui) == len(result)
        for i in range(len(result)):
            assert result[i] == result_book_ui[i]
