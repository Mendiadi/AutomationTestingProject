
import allure
import pytest
from commons.utils import log_name


@pytest.mark.usefixtures("author_setup")
@allure.epic("UI Author Page")
class TestAuthorPage:

    @log_name
    def test_validate_books(self):
        pytest.skip()
        pass

    @log_name
    def test_validate_name_headline(self):
        pytest.skip()
        pass

    @log_name
    def test_validate_data_vs_database(self):
        pytest.skip()
        pass

    @log_name
    def validate_data_updated_in_books(self):
        pytest.skip()
        pass

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
