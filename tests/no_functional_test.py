import logging
import allure
LOGGER = logging.getLogger(__name__)


@allure.epic("UI Readability of buttons tests")
class TestReadability:

    @allure.title("verify login section buttons readability")
    def test_readability_of_buttons_login(self, get_main_page):
        submit_btn_text = get_main_page.get_submit_btn_text()
        register_btn_text = get_main_page.get_register_btn_text()
        register_page = get_main_page.click_register()
        back_to_login_text = register_page.get_back_login_btn_text()
        assert submit_btn_text == "Submit"
        assert register_btn_text == "Register!"
        assert back_to_login_text == "Back To Login"

    @allure.title("verify base layer buttons are readability")
    def test_readability_of_buttons_base(self, get_main_page):
        book_stor_btn_txt = get_main_page.get_book_store_btn_text()
        store_btn_txt = get_main_page.get_store_btn_text()
        login_btn_txt = get_main_page.get_login_btn_text()
        LOGGER.info(book_stor_btn_txt)
        LOGGER.info(store_btn_txt)
        LOGGER.info(login_btn_txt)
        assert "Book Store" in book_stor_btn_txt
        assert "Log In" in login_btn_txt
        assert "Store" in store_btn_txt