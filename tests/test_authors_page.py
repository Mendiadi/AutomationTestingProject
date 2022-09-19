import allure
import pytest
from commons.utils import log_name
@allure.epic("UI Authors Page")
class TestAuthorsPage:
    @log_name
    def test_url(self,main_page):
        authors_page = main_page.click_authors_btn()
        assert authors_page.url.endswith("authors")

    @log_name
    def test_add_author_apear(self):
        pytest.skip()
        pass

    @log_name
    def test_update_author_apear(self):
        pytest.skip()
        pass

    @log_name
    def test_delete_author_apear(self):
        pytest.skip()
        pass

    @log_name
    def test_validate_authors_vs_database(self):
        pytest.skip()
        pass