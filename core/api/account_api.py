import allure
from core.api import rest
from core.models import AuthResponseDto
from core.api.base_api import BaseAPI
from core.api.constant import api_links


class AccountApi(BaseAPI):

    def __init__(self, url: str, session):
        super().__init__(url, session)

    @allure.step("Register from api")
    @rest.post(url=api_links["register"], data_t=rest.JSON)
    def register(self, acc):
        return self.as_dict(acc)

    @allure.step("Login from api")
    @rest.post(url=api_links['login'], data_t=rest.JSON)
    def login(self, user) -> [AuthResponseDto, dict]:
        if self._response.ok:
            return AuthResponseDto(**self._response.json())
        return self.as_dict(user)

    @allure.step("refresh from api")
    @rest.post(url=api_links['token'], data_t=rest.JSON)
    def refresh_token(self, user):
        if self._response.ok:
            return {'res': AuthResponseDto(**self._response.json()), 'code': self._response.status_code}
        return self.as_dict(user)
