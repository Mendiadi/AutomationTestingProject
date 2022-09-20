import allure
import pytest
from commons.utils import log_name


@allure.epic("UI Readability of buttons tests")
class TestReadability:

    @log_name
    @allure.title("verify login section buttons readability")
    def test_readability_of_buttons_login(self, main_page):
        submit_btn_text = main_page.get_submit_btn_text()
        register_btn_text = main_page.get_register_btn_text()
        register_page = main_page.click_register()
        back_to_login_text = register_page.get_back_login_btn_text()
        assert submit_btn_text == "Submit"
        assert register_btn_text == "Register!"
        assert back_to_login_text == "Back To Login"

    @log_name
    @allure.title("verify base layer buttons are readability")
    def test_readability_of_buttons_base(self, main_page):
        book_stor_btn_txt = main_page.get_book_store_btn_text()
        store_btn_txt = main_page.get_store_btn_text()
        login_btn_txt = main_page.get_login_btn_text()
        assert "Book Store" in book_stor_btn_txt
        assert "Log In" in login_btn_txt
        assert "Store" in store_btn_txt

    @log_name
    @allure.title("check login page placeholders for entries")
    def test_read_placeholder_login_page(self, main_page):
        assert main_page.get_email_placeholder() == "Enter email"
        assert main_page.get_password_placeholder() == "Password"

    @log_name
    @allure.title("readability of buttons in base layer")
    def test_readability_of_buttons_author_page(self, main_page):
        assert main_page.get_login_btn_text() == "Log In"
        assert "Book Store" in main_page.get_book_store_btn_text()
        assert main_page.get_store_btn_text() == "Store"
        assert main_page.get_authors_btn_text() == "Authors"
        assert main_page.get_search_btn_text() == "Search"


@allure.epic("UI Loading tests")
@pytest.mark.smoke
class TestSmoke:
    @log_name
    @allure.title("verify open page")
    def test_page_open(self, main_page):
        excepted_title = "React App"
        assert main_page.title == excepted_title

    @log_name
    @allure.title("sanity login page nad register load properly")
    def test_login_page_loading_elements(self, main_page):
        login_result = main_page.elements_visible_login()
        register_page = main_page.click_register()
        register_result = register_page.element_visible_register()
        results = (register_result, login_result)
        for result in results:
            for element_is_found in result:
                assert element_is_found
