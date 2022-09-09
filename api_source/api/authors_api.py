from api_source.core import rest
from api_source.api.base_api import BaseAPI
from api_source.models.author import Author


class AuthorsApi(BaseAPI):
    def __init__(self, url: str, session):
        super().__init__(url, session)

    @rest.post(data_t=rest.JSON)
    def post_authors(self):
        if self.__response.ok:
            return Author(**self.__response.json())
        return self.as_dict(self.__response.status_code, self.__response.text)

    @rest.get()
    def get_authors(self):
        if self.__response.ok:
            authors_list = []
            for author in self.__response.json():
                authors_list.append(Author(**author))
            return authors_list
        return self.as_dict(self.__response.status_code, self.__response.text)

    @rest.delete(param="id")
    def delete_author(self):
        return self.as_dict(self.__response.status_code, self.__response.text)
