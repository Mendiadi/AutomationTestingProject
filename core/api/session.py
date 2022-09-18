import requests
from commons.utils import log_data

class SessionContextManager:
    """
        Context Manager to make a session
        and simply auto closed and logs after session ends
    """

    def __init__(self, headers: [] = ""):
        self._headers = headers
        self._session = requests.session()

    def __enter__(self):
        self._session.headers.update(self._headers)
        log_data(f"session started... {self._session.headers.items()}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()
        log_data(f"""session closed.. cookies = {self._session.cookies.items()}
                       auth = {self._session.auth} headers = {self._session.headers.items()}
                         exe_type: {exc_type},exe_val {exc_val}, exe_tb {exc_tb}""")


class Session(SessionContextManager):
    """
        Session Context Manager class
        to make some operations on session

    """
    # HEADERS = {"accept": "application/json", 'Authorization': f'Bearer %'}

    def __init__(self, headers: {...} = ""):
        super().__init__(headers)
        self._headers = headers
        self._login_url = 0

    def set_login_url(self, url: str) -> None:
        self._login_url = url

    @property
    def session(self) -> requests.Session:
        return self._session

    @property
    def headers(self) -> {...}:
        return self._session.headers

    def update_token(self, user, is_created_now=False) -> [int]:
        """
        Update the login user and authorize
        create new users if database are empty
        save the results in file
        :param user: user data to login
        :param is_created_now: true if user are just created and need to store it
        :return: None ot status code
        """
        from commons import utils
        log_data(f"session token updated with account {user}")
        if isinstance(user, str):
            headers = {'Authorization': f'Bearer {user}'}
            self._session.headers.update(headers)
            return
        try:
            user_ = user['user']
        except KeyError:
            user_ = user
        finally:
            res = self._session.post(url=self._login_url, json=user_)
        if is_created_now:
            user["main_user_id"] = res.json()["userId"]
            user_dict = {"id": res.json()["userId"]}
            utils.write_to_json(user_dict, r"tests\user_id.json")
        try:
            token = res.json()['token']
        except KeyError:
            token = res
        headers = {"accept": "application/json", 'Authorization': f'Bearer {token}'}
        self._session.headers.update(headers)
        return res.status_code
