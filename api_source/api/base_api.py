from api_source.core import rest


class BaseAPI:
    def __init__(self, url: str, headers,session):
        self._base_url = url
        self._headers = headers
        self._session = session


