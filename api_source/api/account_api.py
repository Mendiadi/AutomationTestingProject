from api_source.core import rest
from api_source.models.auth_response_dto import AuthResponseDto
from api_source.api.base_api import BaseAPI
from api_source.core.constant import api_links


class AccountApi(BaseAPI):

    def __init__(self, url: str, session):
        super().__init__(url, session)

    @rest.post(url=api_links["register"], data_t=rest.JSON)
    def register(self):
        return self.as_dict(self.__response.status_code, self.__response.text)

    @rest.post(url=api_links['login'], data_t=rest.JSON)
    def login(self) -> AuthResponseDto:
        if self.__response.ok:
            return AuthResponseDto(**self.__response.json())
        return self.as_dict(self.__response.status_code, self.__response.text)

    @rest.post(url=api_links['token'], data_t=rest.JSON)
    def refresh_token(self):
        if self.__response.ok:
            return self.__response.text
        return self.as_dict(self.__response.status_code, self.__response.text)

