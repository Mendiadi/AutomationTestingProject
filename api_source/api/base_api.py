from api_source.core import rest


class BaseAPI:
    def __init__(self, url: str, headers):
        self._base_url = url
        self._headers = headers
        self._session = rest.get_session(self._headers)


