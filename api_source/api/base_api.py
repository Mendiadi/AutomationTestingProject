from api_source.core.requests_factory import Rest


class BaseAPI:
    def __init__(self, url: str, headers):
        self._base_url = url
        self._get_url = url
        self._post_url = url
        self._delete_url = url
        self._put_url = url
        self._headers = headers
        self._session = Rest.get_session(self._headers)

