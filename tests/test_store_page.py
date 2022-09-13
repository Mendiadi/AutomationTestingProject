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
    def test_buy_no_login_book(self, get_main_page):
        store_page = get_main_page.click_bookstore()
        time.sleep(3)
        book = store_page.get_book(title="1984")
        time.sleep(3)
        msg = store_page.purchase(book)

        LOGGER.info(msg)
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

    def test_books_apear(self):
        pass

    @allure.title("case post books and see if they apear at screen")
    def test_books_updated(self,get_main_page,book_api,random_data,authors_api):
        author_new = random_data.generate_author("moshe")
        author = authors_api.post_authors(author_new)
        book_created = random_data.generate_book(name="moshe is hot", authorid=author.id)
        book_api.post_books(book_created)
        store_page = get_main_page.click_bookstore()
        books = store_page.get_books_by_author("moshe")
        for book in books:
            text = store_page.get_book_title(book)
            assert "moshe is hot" == text

