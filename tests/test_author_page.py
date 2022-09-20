
import allure
import pytest
from commons.utils import log_name

# if you make login and close window after its will log out you and the logout btn still show up bug

@pytest.mark.usefixtures("author_setup")
@allure.epic("UI Author Page")
class TestAuthorPage:

    @log_name
    @allure.title("case validate books apear ")
    def test_validate_books(self,main_page,api,data):
        for i in range(3):
            api.books.post_books(data.generate_book(authorid=self.author.id))
        books_api = api.books.find_book_by_author_id(authorId=self.author.id)
        authors_page = main_page.click_authors_btn()
        authors_page.reload()
        author = authors_page.find_author_by_name(self.author)
        author_page = authors_page.go_to_author(author)
        books_ui_names_author = [(author_page.get_book_title(book),
                           author_page.get_book_author(book)) for book in author_page.get_books()]
        books_api_names = [book.name for book in books_api]
        for book_title,book_author in books_ui_names_author:
            assert book_title in books_api_names
            assert self.author.name in book_author


    @log_name
    @allure.title("validate headline show name")
    def test_validate_name_headline(self,api,data,main_page):
        authors_page = main_page.click_authors_btn()
        author = authors_page.find_author_by_name(self.author.name)
        author_page = authors_page.go_to_author(author)
        assert self.author.name == author_page.get_headline()


    @log_name
    def test_validate_data_vs_database(self):
        pytest.skip()
        pass

    @log_name
    def test_data_updated_in_books(self,api,data,main_page):
        book = api.books.post_books(data.generate_book(authorid=self.author.id))
        authors_page = main_page.click_authors_btn()
        authors_page.reload()
        author = authors_page.find_author_by_name(self.author)
        author_page = authors_page.go_to_author(author)
        books_ui = author_page.get_book(book.name)
        book_api = api.books.get_book_by_id(id=book.id)
        assert author_page.get_book_title(books_ui) == book_api.name
        book_api.amountInStock = 100
        book_api.name = "yossi"
        api.books.put_book(book_api,id=book_api.id)
        authors_page.reload()
        books_ui = author_page.get_book(book_api.name)
        assert author_page.get_book_title(books_ui) == "yossi"
        assert "100" in author_page.get_book_stock(books_ui)

    @log_name
    def test_add_and_delete_books(self):
        pytest.skip()
        pass

    @log_name
    def test_validate_home_location_updated(self):
        pytest.skip()
        pass

    @log_name
    def test_validate_map_cordinate(self, main_page, api, data):
        authors_page = main_page.click_authors_btn()
        author = authors_page.find_author_by_name(name=self.author.name)
        author_page = authors_page.go_to_author(author)
        map = author_page.on_map()
        la, lo = map.get_map_cordin_in_float()
        author_page.out_map(map)
        author = api.authors.get_author_by_id(id=self.author.id)
        assert author.homeLatitude == la
        assert author.homeLongitude == lo

    @log_name
    def test_map_change_look(self, main_page, data, api):
        authors_page = main_page.click_authors_btn()
        author = authors_page.find_author_by_name(name=self.author.name)
        author_page = authors_page.go_to_author(author)
        map = author_page.on_map()
        map_cor = map.get_map_details()
        change_look_style = map.change_look_style()
        api.authors.delete_author(id=self.author.id)
        assert change_look_style != "Show street map"
        change_look_style_again = map.change_look_style()
        assert change_look_style_again != "Show satellite imagery"
