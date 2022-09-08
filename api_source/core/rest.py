import requests

GET = "GET"
POST = "POST"
PUT = "PUT"
DELETE = "DELETE"


def get_session(headers="") -> requests.Session:
    session__ = requests.session()
    session__.headers.update(headers)
    return session__


def get_response(type, ptr__, url, data):
    if type is POST:
        return ptr__.post(url=url, json=data)
    elif type is GET:
        return ptr__.get(url=url, data=data)
    elif type is DELETE:
        return ptr__.delet(url=url, data=data)
    elif type is PUT:
        return ptr__.put(url=url, data=data)
    else:
        raise


def parse(url, kw, param, self):
    data = kw['data'] if "data" in kw else None
    param_ = kw[param] if param else ""
    url_ = self._base_url + url if url else self._base_url
    return data, param_, url_


def request(type_, url=None, param=None):
    def decorate(func, **kwargs):
        def wrapper(self, *args, **kwargs):
            data, param_, url_ = parse(url, kwargs, param, self)
            response = get_response(type_, self._session, url_, data)
            return func(self, response=response)

        return wrapper

    return decorate


def get(url=None, param=None):
    return request(GET, url, param)


def delete(url=None, param=None):
    return request(DELETE, url, param)


def post(url=None, param=None):
    return request(POST, url, param)


def put(url=None, param=None):
    return request(PUT, url, param)


def as_dict(code, msg):
    return {"code": code, "msg": msg}
