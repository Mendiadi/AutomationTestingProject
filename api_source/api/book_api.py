from api_source.api.base_api import BaseAPI
from api_source.core import rest
from api_source.models.book import Book
import allure
class BookApi(BaseAPI):
    def __init__(self, url: str, session):
        super().__init__(url, session)

    @allure.step("get books from api")
    @rest.get()
    def get_books(self) -> list[Book]:
        if self._response.ok:
            books = []
            for book in self._response.json():
                books.append(book)
            return books
        return self.as_dict()
