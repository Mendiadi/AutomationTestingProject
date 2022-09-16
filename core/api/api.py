from core.api import BookApi,AccountApi,AuthorsApi
from core.api.constant import *
from core.api.rest import Session
class API:
    """
        All services endpoints in one place
    """

    def __init__(self,**kwargs):
        self._services = kwargs
        self._book = self._services['books']
        self._account = self._services['account']
        self._authors = self._services['authors']
        self._session = self._services['session']

    def __str__(self):
        return f"api services: {self._services}"

    @property
    def session(self) -> Session:
        return self._session

    @property
    def books(self) -> BookApi:
        return self._book

    @property
    def account(self) -> AccountApi:
        return self._account

    @property
    def authors(self) -> AuthorsApi:
        return self._authors


