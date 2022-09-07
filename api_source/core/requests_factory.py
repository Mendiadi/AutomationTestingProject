import requests


class Rest:

    @staticmethod
    def get_session(headers) -> requests.Session:
        session__ = requests.session()
        session__.headers.update(headers)
        return session__

    @staticmethod
    def get(func):
        def wrapper(self, **kwargs):
            if kwargs['data'] == "":
                kwargs['data'] = None
            response = self._session.get(url=f"{self._get_url}/{kwargs['id']}", data=kwargs['data'])
            return func(self, response=response)

        return wrapper

    @staticmethod
    def delete(func):
        def wrapper(self, **kwargs):
            if kwargs['data'] == "":
                kwargs['data'] = None
            response = self._session.delete(url=f"{self._delete_url}/{kwargs['id']}", data=kwargs['data'])

            return func(self, response=response)

        return wrapper

    @staticmethod
    def post(func):
        def wrapper(self, **kwargs):
            if kwargs['data'] == "":
                kwargs['data'] = None
            response = self._session.post(url=f"{self._post_url}/", data=kwargs['data'])

            return func(self, response=response)

        return wrapper

    @staticmethod
    def put(func):
        def wrapper(self, **kwargs):
            if kwargs['data'] == "":
                kwargs['data'] = None
            response = self._session.put(url=f"{self._put_url}/{kwargs['id']}", data=kwargs['data'])

            return func(self, response=response)


        return wrapper

    @staticmethod
    def res_dict(code, msg):
        return {"code": code, "msg": msg}