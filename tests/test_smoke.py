import allure
import pytest
from commons.utils import log_name


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
    def test_login_page_loading_elements(self,main_page):
        login_result = main_page.elements_visible_login()
        register_page = main_page.click_register()
        register_result = register_page.element_visible_register()
        results = (register_result,login_result)
        for result in results:
            for element_is_found in result:
                assert element_is_found

    @log_name
    def test_store_element_loading(self,main_page):
        pytest.skip()


    @log_name
    def test_authors_element_loading(self,main_page):
        pytest.skip()


    @log_name
    def test_authors_page_loading_elements(self):
        pytest.skip()


    @log_name
    def test_base_page_load_element(self):
        pytest.skip()




