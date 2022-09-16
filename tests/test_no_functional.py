
import allure
from commons.utils import log_name
import  pytest

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
    def test_readability_of_buttons_store(self):
        pytest.skip()
        pass

    @log_name
    def test_readability_of_buttons_authors(self):
        pytest.skip()
        pass

    @log_name
    def test_readability_of_buttons_author_page(self):
        pytest.skip()
        pass
