
import logging
import allure
LOGGER = logging.getLogger(__name__)


@allure.epic("UI Readability")
class TestReadability:

    @allure.title("verify login section buttons readability")
    def test_readability_of_buttons(self, get_main_page):
        submit_btn_text = get_main_page.get_submit_btn_text()
        register_btn_text = get_main_page.get_register_btn_text()
        register_page = get_main_page.click_register()
        back_to_login_text = register_page.get_back_login_btn_text()
        assert submit_btn_text == "Submit"
        assert register_btn_text == "Register!"
        assert back_to_login_text == "Back To Login"

