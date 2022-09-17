from core.api import BookAPI, AccountAPI, AuthorsAPI
from core.api import session as se
from commons.utils import log_data


class Services:
    """
        holder class for services endpoints in one place
    """

    @property
    def books(self) -> BookAPI:
        return self._books_

    @property
    def account(self) -> AccountAPI:
        return self._account_

    @property
    def authors(self) -> AuthorsAPI:
        return self._authors_

    @property
    def session(self) -> se.Session:
        return self._session_

    def __str__(self):
        return f"api services: {[f'{name} : {service}' for name, service in self.__dict__.items()]}"

    def __getattribute__(self, item):
        return super(Services, self).__getattribute__(item)

    def __getattr__(self, item):
        log_data(f"{__name__} set service {item}")
        return super(Services, self).__setattr__(item)

    def __setitem__(self, key, value):
        setattr(self, key, value)
