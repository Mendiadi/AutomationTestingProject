import logging
import allure
import pytest

LOGGER = logging.getLogger(__name__)


@allure.epic("UI store page")
class TestStore:

    @allure.title("case add book and verify is apear in page ")
    def test_add_book_apear(self, get_main_page, api, data):
        author_created = data.generate_author()
        author = api.authors.post_authors(author_created)
        book_created = data.generate_book(authorid=author.id, imageUrl=True)
        book = api.books.post_books(book_created)
        store_page = get_main_page.click_bookstore()
        store_page.reload()
        book_elem = store_page.get_book(title=book.name)
        book_title = store_page.get_book_title(book_elem)
        book_author = store_page.get_book_author(book_elem)
        LOGGER.info(f"title: {book_title} author: {book_author}")
        assert author.name in book_author
        assert book_created.name == book.name
        api.authors.delete_author(id=author.id)

    @allure.title("case buy book without login")
    def test_buy_no_login_book(self, get_main_page, api, data):
        author_created = data.generate_author()
        author = api.authors.post_authors(author_created)
        book_created = data.generate_book(authorid=author.id, name="shay", imageUrl=True)
        book = api.books.post_books(book_created)
        store_page = get_main_page.click_bookstore()
        store_page.reload()
        book1 = store_page.get_book(title=book_created.name)
        LOGGER.info(book1)
        msg = store_page.purchase(book1)
        LOGGER.info(msg)
        assert book.amountInStock == api.books.get_book_by_id(id=book.id).amountInStock
        assert "Must be signed in to purchase." in msg
        api.authors.delete_author(id=author.id)

    @allure.title("get books by author")
    def test_update_and_get_books_by_author(self, get_main_page):
        store_page = get_main_page.click_bookstore()
        books = store_page.get_books_by_author("George Orwell")
        for book in books:
            book_title = store_page.get_book_title(book)
            LOGGER.info(book_title)
            assert book_title == "1984" or "Animal Farm"

    @allure.title("case buy book with login and created book")
    def test_case_buy_book(self, get_main_page, api, data, get_test_data):
        get_main_page.login(get_test_data.email, get_test_data.password).click_bookstore()
        author = api.authors.post_authors(data.generate_author())
        book = api.books.post_books(data.generate_book(authorid=author.id))
        store_page = get_main_page.click_bookstore()
        store_page.reload()
        book1 = store_page.get_book(title=book.name)
        LOGGER.info(book1)
        msg = store_page.purchase(book1)
        store_page.reload()
        amount_in_stock_api = api.books.get_book_by_id(id=book.id).amountInStock
        book_after_buy = store_page.get_book(title=book.name)
        amount_in_stock_ui = store_page.get_book_stock(book_after_buy)
        LOGGER.info(amount_in_stock_api)
        assert str(book.amountInStock - 1) in amount_in_stock_ui
        assert book.amountInStock - 1 == amount_in_stock_api
        assert f"Thank you for your purchase of {book.name}" in msg
        api.authors.delete_author(id=author.id)

    @allure.title("case buy book from api and check for update")
    def test_buy_book_from_api_to_ui(self, data, api, get_test_data, get_main_page):
        author_created = data.generate_author()
        author = api.authors.post_authors(author_created)
        book_created = data.generate_book(name="waves of sea", authorid=author.id, imageUrl=True)
        book = api.books.post_books(book_created)
        store_page = get_main_page.click_bookstore()
        book_element = store_page.get_book(title=book.name)
        book_element_stock_before = store_page.get_book_stock(book_element)
        api.books.purchase_book(id=book.id)
        store_page.reload()
        book_element_after = store_page.get_book(book.name)
        book_element_stock_after = store_page.get_book_stock(book_element_after)
        assert book_element_stock_before != book_element_stock_after
        api.authors.delete_author(id=author.id)

    @allure.title("case post books and see if they apear at screen")
    def test_books_updated(self, get_main_page, api, data):
        author_new = data.generate_author("moshe")
        author = api.authors.post_authors(author_new)
        book_created = data.generate_book(name="moshe is hot", authorid=author.id, imageUrl=True)
        api.books.post_books(book_created)
        store_page = get_main_page.click_bookstore()
        books = store_page.get_books_by_author("moshe")
        for book in books:
            text = store_page.get_book_title(book)
            assert "moshe is hot" == text
        api.authors.delete_author(id=author.id)

    @allure.title("check if all the books in db are visible")
    def test_verify_books(self, get_main_page, api):
        boos_api = api.books.get_books()
        store_page = get_main_page.click_bookstore()
        books = store_page.get_books()
        LOGGER.info(books)
        LOGGER.info(boos_api)
        result_book_ui = [store_page.get_book_title(book) for book in books]
        result = [book.name for book in boos_api]
        assert len(result_book_ui) == len(result)
        for i in range(len(result)):
            assert result[i] == result_book_ui[i]

    def test_finish_book_stock(self):
        pytest.skip()
        pass

    def test_buy_book_that_no_stock(self):
        pytest.skip()
        pass

    def test_buy_book_no_stock_and_login(self):
        pytest.skip()
        pass

    @allure.title("post 10 new books and buy all the books in the store once ")
    def test_buy_multiple(self, get_main_page, get_test_data, data, api):
        author_created = data.generate_author()
        author = api.authors.post_authors(author_created)
        for i in range(5):
            book = data.generate_book(authorid=author.id)
            api.books.post_books(book)
        login_page = get_main_page.login(get_test_data.email, get_test_data.password)
        store_page = login_page.click_bookstore()
        get_main_page.reload()
        books = store_page.get_books()
        for book in books:
            store_page.purchase(book)
            LOGGER.info(store_page.get_book_title(book))
        api.authors.delete_author(id=author.id)

    @allure.title("verify that book image updated in ui")
    def test_book_image_change(self, get_main_page, api, data):
        author_created = data.generate_author(name="dor dayan")
        author = api.authors.post_authors(author_created)
        book_created = data.generate_book(authorid=author.id, imageUrl=True)
        book_before = api.books.post_books(book_created)
        store_page = get_main_page.click_bookstore()
        store_page.reload()
        book_from_ui = store_page.get_book(title=book_before.name)
        book_before_img = store_page.get_book_image_url(book_from_ui)
        assert book_before_img == book_before.imageUrl
        book_before.imageUrl = data.image_temp()
        api.books.put_book(book_before.convert_to_book_dto(), id=book_before.id)
        store_page.reload()
        book_after = store_page.get_book(title=book_before.name)
        book_after_img = store_page.get_book_image_url(book_after)
        assert book_after_img != book_before_img and book_after_img == data.image_temp()
        api.authors.delete_author(id=author.id)

    @allure.title("verify that book in ui as same data as db")
    def test_book_data_same_as_db(self, get_main_page, data, api):
        author_new = data.generate_author("david")
        author = api.authors.post_authors(author_new)
        book_created = data.generate_book(name="im happy", authorid=author.id,
                                          description="My first day in earth", price="30", amount="5",
                                          imageUrl=True)
        book_ = api.books.post_books(book_created)
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
        api.books.put_book(book_.convert_to_book_dto(), id=book_.id)
        store_page.reload()
        book_after = store_page.get_book(title=book_.name)
        assert store_page.get_book_decription(book_after) == "im love you"
        api.authors.delete_author(id=author.id)
