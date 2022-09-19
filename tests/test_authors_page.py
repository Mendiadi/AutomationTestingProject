import allure
from commons.utils import log_name


@allure.epic("UI Authors Page")
class TestAuthorsPage:
    @log_name
    @allure.title("test url ")
    def test_url(self, main_page):
        authors_page = main_page.click_authors_btn()
        assert authors_page.url.endswith("authors")

    @log_name
    @allure.title("case add author and see if apear")
    def test_add_author_apear(self, author_setup, main_page):
        authors_page = main_page.click_authors_btn()
        authors = authors_page.get_authors()
        assert self.author.name in [authors_page.get_author_name(author) for author in authors]

    @log_name
    @allure.title("case change author name and see if ui update ")
    def test_update_author_apear(self, author_setup, main_page, api):
        authors_page = main_page.click_authors_btn()
        authors = authors_page.get_authors()
        assert self.author.name in [authors_page.get_author_name(author) for author in authors]
        self.author.name = "adi"
        api.authors.put_author_by_id(self.author, id=self.author.id)
        authors_page.reload()
        authors = authors_page.get_authors()
        assert "adi" in [authors_page.get_author_name(author) for author in authors]

    @log_name
    @allure.title("case delete author and see if its deleted in ui")
    def test_delete_author_apear(self, main_page, api, data):
        author = api.authors.post_authors(data.generate_author(name="adi"))
        authors_page = main_page.click_authors_btn()
        authors_page.reload()
        authors = authors_page.get_authors()
        assert author.name in [authors_page.get_author_name(author) for author in authors]
        api.authors.delete_author(id=author.id)
        authors_page.reload()
        authors = authors_page.get_authors()
        assert "adi" not in [authors_page.get_author_name(author) for author in authors]

    @log_name
    @allure.title("case check if ui show all authors properly")
    def test_validate_authors_vs_database(self, api, main_page):
        authors_api = api.authors.get_authors()
        authors_page = main_page.click_authors_btn()
        authors__names_ui = [authors_page.get_author_name(author) for author in authors_page.get_authors()]
        assert all(map(lambda author: author.name in authors__names_ui, authors_api))
