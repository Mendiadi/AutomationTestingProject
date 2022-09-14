import logging
import time
import allure

LOGGER = logging.getLogger(__name__)


@allure.epic("UI store page")
class TestStore:

    @allure.title("case add book and verify is apear in page ")
    def test_add_book_apear(self, get_main_page,book_api,authors_api,random_data):
        author_created = random_data.generate_author()
        author = authors_api.post_authors(author_created)
        book_created = random_data.generate_book(authorid=author.id)
        book = book_api.post_books(book_created)
        store_page = get_main_page.click_bookstore()
        store_page.reload()
        book_elem = store_page.get_book(title=book.name)
        book_title = store_page.get_book_title(book_elem)
        book_author = store_page.get_book_author(book_elem)
        LOGGER.info(f"title: {book_title} author: {book_author}")
        assert author.name in book_author
        assert book_created.name == book.name

    @allure.title("case buy book without login")
    def test_buy_no_login_book(self, get_main_page, book_api, random_data, authors_api):
        author_created = random_data.generate_author()
        author = authors_api.post_authors(author_created)
        book_created = random_data.generate_book(authorid=author.id, name="shay")
        book = book_api.post_books(book_created)
        store_page = get_main_page.click_bookstore()
        store_page.reload()
        book1 = store_page.get_book(title=book_created.name)
        LOGGER.info(book1)
        msg = store_page.purchase(book1)
        LOGGER.info(msg)
        assert book.amountInStock == book_api.get_book_by_id(id=book.id).amountInStock
        assert "Must be signed in to purchase." in msg

    @allure.title("get books by author")
    def test_update_and_get_books_by_author(self, get_main_page):
        store_page = get_main_page.click_bookstore()
        books = store_page.get_books_by_author("George Orwell")
        for book in books:
            book_title = store_page.get_book_title(book)
            LOGGER.info(book_title)
            assert book_title == "1984" or "Animal Farm"

    @allure.title("case buy book with login and created book")
    def test_case_buy_book(self, get_main_page, book_api, random_data, authors_api, get_test_data):
        get_main_page.login(get_test_data.email, get_test_data.password).click_bookstore()
        author_created = random_data.generate_author()
        author = authors_api.post_authors(author_created)
        book_created = random_data.generate_book(authorid=author.id)
        book = book_api.post_books(book_created)
        store_page = get_main_page.click_bookstore()
        store_page.reload()
        book1 = store_page.get_book(title=book_created.name)
        LOGGER.info(book1)
        msg = store_page.purchase(book1)
        amount_in_stock_api = book_api.get_book_by_id(id=book.id).amountInStock
        store_page.reload()
        book_after_buy = store_page.get_book(title=book.name)
        amount_in_stock_ui = store_page.get_book_stock(book_after_buy)
        LOGGER.info(amount_in_stock_api)
        assert str(book.amountInStock - 1) in amount_in_stock_ui
        assert book.amountInStock - 1 == amount_in_stock_api
        assert f"Thank you for your purchase of {book.name}" in msg

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


    def test_buy_book_that_no_stock(self):
        pass

    def test_buy_book_no_stock_and_login(self):
        pass

    @allure.title("post 10 new books and buy all the books in the store once ")
    def test_buy_multiple(self,get_main_page,get_test_data,random_data,authors_api,book_api):
        author_created = random_data.generate_author()
        author = authors_api.post_authors(author_created)
        for i in range(10):
            book = random_data.generate_book(authorid=author.id)
            book_api.post_books(book)
        get_main_page.reload()
        login_page = get_main_page.login(get_test_data.email,get_test_data.password)
        store_page = login_page.click_bookstore()
        books = store_page.get_books()
        for book in books:
            store_page.purchase(book)
            LOGGER.info(store_page.get_book_title(book))


    def test_book_data_same_as_db(self,get_main_page,random_data,book_api,authors_api):
        author_new = random_data.generate_author("david")
        author = authors_api.post_authors(author_new)
        book_created = random_data.generate_book(name="im happy", authorid=author.id,
                                    description="My first day in earth",price="30",amount="5")
        book_ = book_api.post_books(book_created)
        store_page = get_main_page.click_bookstore()
        store_page.reload()
        book = store_page.get_book(title="im happy")
        b_title = store_page.get_book_title(book)
        b_author = store_page.get_book_author(book)
        b_desc = store_page.get_book_decription(book)
        b_price = store_page.get_book_price(book)
        b_stock = store_page.get_book_stock(book)
        assert "im happy" == b_title and "david" in b_author and \
            b_desc == "My first day in earth" and "30" in b_price and "5" in b_stock
        LOGGER.info(f"{b_title}, {b_stock},{b_author},{b_price},{b_desc}")
        book_.description = "im love you"
        book_api.put_book(book_.convert_to_book_dto(),id=book_.id)
        store_page.reload()
        book_after = store_page.get_book(title=book_.name)
        assert store_page.get_book_decription(book_after) == "im love you"