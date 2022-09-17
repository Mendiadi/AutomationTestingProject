import allure
from core.api import rest
from core.models import AuthResponseDto
from core.api.base_api import BaseAPI
from core.api.constant import api_links
from typing import Mapping

class AccountAPI(BaseAPI):

    def __init__(self, url: str, session: rest.Session):
        super().__init__(url, session)

    @rest.post(url=api_links["register"], data_t=rest.JSON)
    def register(self, acc: Mapping[str, ...]) -> ... - Mapping[str, ...]:
        with allure.step(f"Register {acc} from api"):
            return self.as_dict(acc)

    @rest.post(url=api_links['login'], data_t=rest.JSON)
    def login(self, user: Mapping[str, ...]) -> ... - [AuthResponseDto, dict]:
        with allure.step(f"Login to {user} from api"):
            if self._response.ok:
                return AuthResponseDto(**self._response.json())
            return self.as_dict(user)

    @rest.post(url=api_links['token'], data_t=rest.JSON)
    def refresh_token(self, user: Mapping[str, ...]) -> ... - [AuthResponseDto, dict]:
        with allure.step(f"refresh token to  {user}"):
            if self._response.ok:
                return {'res': AuthResponseDto(**self._response.json()), 'code': self._response.status_code}
            return self.as_dict(user)
