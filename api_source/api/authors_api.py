from api_source.core import rest
from api_source.api.base_api import BaseAPI
from api_source.models.author import Author
from api_source.models.get_author_dto import GetAuthorDto
import allure


class AuthorsApi(BaseAPI):
    def __init__(self, url: str, session):
        super().__init__(url, session)

    @allure.step("post authors from api")
    @rest.post(data_t=rest.JSON)
    def post_authors(self, author: GetAuthorDto):
        if self._response.ok:
            return Author(**self._response.json())
        return self.as_dict(author)

    @allure.step("get authors from api")
    @rest.get()
    def get_authors(self):
        if self._response.ok:
            authors_list = []
            for author in self._response.json():
                authors_list.append(Author(**author))

            return authors_list
        return self.as_dict()

    @rest.delete(param="id")
    def delete_author(self, id: int):
        with allure.step(f"delete author id={id}"):
            return self.as_dict(id)

    @rest.get(param="id")
    def get_author_by_id(self, id: int):
        if self._response.ok:
            return Author(**self._response.json())
        return self.as_dict(id)

    @rest.put(param="id", data_t=rest.JSON)
    def put_author_by_id(self, author, id: int):
        with allure.step(f"update author {id}"):
            return self.as_dict(author)

    @rest.get(url='/search/', param="query")
    def search(self, query: str):
        with allure.step(f"search for {query}"):
            authors = []
            for author in self._response.json():
                authors.append(Author(**author))
            return authors
