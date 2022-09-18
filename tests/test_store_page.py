import allure
import pytest
from commons.utils import log_name


@pytest.mark.usefixtures("author_setup", "book_setup")
@allure.epic("UI store page")
class TestStore:

    @log_name
    @allure.title("case add book and verify is apear in page ")
    def test_add_book_apear(self, main_page, api, data):
        book = api.books.post_books(data.generate_book(authorid=self.author.id))
        store_page = main_page.click_bookstore()
        store_page.reload()
        book_elem = store_page.get_book(title=book.name)
        assert self.author.name in store_page.get_book_author(book_elem)
        assert store_page.get_book_title(book_elem) == book.name
        assert book.description == store_page.get_book_decription(book_elem)
        assert str(book.amountInStock) in store_page.get_book_stock(book_elem)
        assert str(book.price) in store_page.get_book_price(book_elem)
        assert book.imageUrl == store_page.get_book_image_url(book_elem)

    @log_name
    @allure.title("case buy book without login")
    def test_buy_no_login_book(self, main_page, api):
        store_page = main_page.click_bookstore()
        store_page.reload()
        book1 = store_page.get_book(title=self.book.name)
        msg = store_page.purchase(book1)
        assert self.book.amountInStock == api.books.get_book_by_id(id=self.book.id).amountInStock
        assert "Must be signed in to purchase." in msg

    @pytest.mark.regression
    @log_name
    @allure.title("get books by author")
    def test_update_and_get_books_by_author(self, main_page, api, data):
        author = api.authors.post_authors(data.generate_author(name="dor david"))
        book_ = api.books.post_books(data.generate_book(authorid=author.id))
        store_page = main_page.click_bookstore()
        store_page.reload()
        books = store_page.get_books_by_author("dor david")
        for book in books:
            book_title = store_page.get_book_title(book)
            assert book_title == "1984" or "Animal Farm"
        api.authors.delete_author(id=author.id)

    @log_name
    @allure.title("case buy book with login and created book")
    def test_case_buy_book(self, main_page, api, data, configuration):
        main_page.login(configuration.email, configuration.password).click_bookstore()
        store_page = main_page.click_bookstore()
        store_page.reload()
        book1 = store_page.get_book(title=self.book.name)
        msg = store_page.purchase(book1)
        store_page.reload()
        amount_in_stock_api = api.books.get_book_by_id(id=self.book.id).amountInStock
        book_after_buy = store_page.get_book(title=self.book.name)
        amount_in_stock_ui = store_page.get_book_stock(book_after_buy)
        assert f"Thank you for your purchase of {self.book.name}" in msg
        assert str(self.book.amountInStock - 1) in amount_in_stock_ui
        assert self.book.amountInStock - 1 == amount_in_stock_api


    @log_name
    @allure.title("case buy book from api and check for update")
    def test_buy_book_from_api_to_ui(self, api, main_page):
        store_page = main_page.click_bookstore()
        book_element = store_page.get_book(title="waves of sea")
        book_element_stock_before = store_page.get_book_stock(book_element)
        api.books.purchase_book(id=self.book.id)
        store_page.reload()
        book_element_after = store_page.get_book(self.book.name)
        book_element_stock_after = store_page.get_book_stock(book_element_after)
        assert book_element_stock_before != book_element_stock_after

    @log_name
    @allure.title("case post books and see if they apear at screen")
    def test_books_updated(self, main_page):
        store_page = main_page.click_bookstore()
        book = store_page.get_book(self.book.name)
        text = store_page.get_book_title(book)
        assert self.book.name == text

    @log_name
    @allure.title("check if all the books in db are visible")
    def test_verify_books(self, main_page, api):
        boos_api = api.books.get_books()
        store_page = main_page.click_bookstore()
        books = store_page.get_books()
        result_book_ui = [store_page.get_book_title(book) for book in books]
        result = [book.name for book in boos_api]
        assert len(result_book_ui) == len(result)
        for i in range(len(result)):
            assert result[i] == result_book_ui[i]

    @log_name
    def test_finish_book_stock(self):
        pytest.skip()

    @log_name
    def test_buy_book_that_no_stock(self):
        pytest.skip()

    @log_name
    def test_buy_book_no_stock_and_login(self):
        pytest.skip()

    @log_name
    @allure.title("post 10 new books and buy all the books in the store once ")
    def test_buy_multiple(self, main_page, configuration, data, api):
        author_created = data.generate_author()
        author = api.authors.post_authors(author_created)
        for i in range(5):
            book = data.generate_book(authorid=author.id)
            api.books.post_books(book)
        login_page = main_page.login(configuration.email, configuration.password)
        store_page = login_page.click_bookstore()
        main_page.reload()
        books = store_page.get_books()
        for book in books:
            store_page.purchase(book)
        api.authors.delete_author(id=author.id)

    @log_name
    @allure.title("verify that book image updated in ui")
    def test_book_image_change(self, main_page, api, data):
        store_page = main_page.click_bookstore()
        store_page.reload()
        book_from_ui = store_page.get_book(title=self.book.name)
        book_before_img = store_page.get_book_image_url(book_from_ui)
        assert book_before_img == self.book.imageUrl
        self.book.imageUrl = data.image_temp()
        api.books.put_book(self.book.convert_to_book_dto(), id=self.book.id)
        store_page.reload()
        book_after = store_page.get_book(title=self.book.name)
        book_after_img = store_page.get_book_image_url(book_after)
        assert book_after_img != book_before_img and book_after_img == data.image_temp()
        api.authors.delete_author(id=self.book.id)

    @log_name
    @allure.title("verify that book in ui as same data as db")
    def test_book_data_same_as_db(self, main_page, data, api):
        book_created = data.generate_book(name="im happy", authorid=self.author.id,
                                          description="My first day in earth", price="30", amount="5",
                                          imageUrl=True)
        book_ = api.books.post_books(book_created)
        store_page = main_page.click_bookstore()
        store_page.reload()
        book = store_page.get_book(title="im happy")
        b_title = store_page.get_book_title(book)
        b_author = store_page.get_book_author(book)
        b_desc = store_page.get_book_decription(book)
        b_price = store_page.get_book_price(book)
        b_stock = store_page.get_book_stock(book)
        assert "im happy" == b_title and self.author.name in b_author and \
               b_desc == "My first day in earth" and "30" in b_price and "5" in b_stock
        book_.description = "im love you"
        api.books.put_book(book_.convert_to_book_dto(), id=book_.id)
        store_page.reload()
        book_after = store_page.get_book(title=book_.name)
        assert store_page.get_book_decription(book_after) == "im love you"
