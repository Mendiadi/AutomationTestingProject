import json
import requests


def get_session(headers) -> requests.Session:
    session__ = requests.session()
    session__.headers.update(headers)
    return session__


def parse(url, kw, param, self):
    data = kw['data'] if "data" in kw else None
    param_ = kw[param] if param else ""
    url_ = self._base_url + url if url else self._base_url
    return data, param_, url_


def get(url=None, param=None):
    def decorate(func, **kwargs):
        def wrapper(self, *args, **kwargs):
            data, param_, url_ = parse(url, kwargs, param, self)
            response = self._session.get(url=url_ + param_, data=data)
            return func(self, response=response)
        return wrapper
    return decorate


def delete(url=None, param=None):
    def decorate(func, **kwargs):
        def wrapper(self, *args, **kwargs):
            data, param_, url_ = parse(url, kwargs, param, self)
            response = self._session.delete(url=url_ + param_, data=data)
            return func(self, response=response)
        return wrapper
    return decorate


def post(url=None, param=None):
    def decorate(func, **kwargs):
        def wrapper(self, *args, **kwargs):
            data, param_, url_ = parse(url, kwargs, param, self)
            response = self._session.post(url=url_ + param_, json=data)
            return func(self, response=response)
        return wrapper
    return decorate


def put(url=None, param=None):
    def decorate(func, **kwargs):
        def wrapper(self, *args, **kwargs):
            data, param_, url_ = parse(url, kwargs, param, self)
            response = self._session.put(url=url_ + param_, data=data)
            return func(self, response=response)
        return wrapper
    return decorate


def res_dict(code, msg):
    return {"code": code, "msg": msg}
