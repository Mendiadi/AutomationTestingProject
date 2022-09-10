from api_source.core import rest
from api_source.models.auth_response_dto import AuthResponseDto
from api_source.api.base_api import BaseAPI
from api_source.core.constant import api_links
import allure

class AccountApi(BaseAPI):

    def __init__(self, url: str, session):
        super().__init__(url, session)

    @allure.step("Register from api")
    @rest.post(url=api_links["register"], data_t=rest.JSON)
    def register(self):
        return self.as_dict(self._response.status_code, self._response.text)

    @allure.step("Login from api")
    @rest.post(url=api_links['login'], data_t=rest.JSON)
    def login(self) -> AuthResponseDto:
        if self._response.ok:
            return AuthResponseDto(**self._response.json())
        return self.as_dict(self._response.status_code, self._response.text)

    @allure.step("refresh from api")
    @rest.post(url=api_links['token'], data_t=rest.JSON)
    def refresh_token(self):
        if self._response.ok:
            return self._response.text
        return self.as_dict(self._response.status_code, self._response.text)

