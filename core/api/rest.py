"""
    Written by adi mendel 6.8.2022
    my implementation for rest api using decorator factory.
    you can send requests from your api class using my decorators as
    @rest.get() - for get request
    @rest.post() for post request
    @rest.delete() for delete request
    @rest.put() for put request
    to use it properly you need to attention for some details!
    (1) you need in your api class method calls to give only one parameter as name 'response' (self also include)
    example (1): in your api class :
                SomeApi():
                    def __init__(self):
                        pass

                    @rest.post()
                    def post_user(self,response):
                        return response # to return the result or return any manipulation
    (2) you can pass the url or just part of it using url param config like that:
    example (2):
            SomeApi():
                def __init__(self):
                    pass

                @rest.post(url="myUrl") # as you can see you can config url
                def post_user(self,response):
                    return response # to return the result or return any manipulation
    (3) also you can config the params to the url mostly like this:
        SomeApi():
                def __init__(self):
                    pass

                @rest.post(url="myUrl",param="name")
                def post_user_name(self,response):
                    return response # to return the result or return any manipulation

                @rest.post(url="myUrl",param="id")
                def post_user_id(self,response):
                    return response # to return the result or return any manipulation

        ** in your test file you use it like:
            def test_user():
                res = post_user_name(name="sample")
                res = post_user_id(id="sample")
                # as you can see you can call these api methods and -
                use the parameter config to send most you need to.

    (4) you can send parameters that will catch as data
    example (4)
        in your test file -
            def test_user():
                res = post_user({name:name,id:id})
                res1 = post_user(user_obj)

    (5) you can always send data with your request
    example (5):
        in your test file -
            def test_user():
                res = post_user(data={name:name,id:id})

                # as you can see you can always send or ignore and then data will be None

    (6) you can choose if you send data by "data=" or "json=" using the data_t arg:
    example (6):
            @rest.post(data_t="json") # for json, its will be default "data" if not sending anything
            def post_user_id(self,response):
                return response # to return the result or return any manipulation

    after im showed you how to use it and example also
    you can simply try and use it its very cool decorators.

    adi.
"""
# implement code start:

import requests
import enum
import logging as lg


# constant variables

class Req(enum.Enum):
    """
        Enum class to store REST operations

    """
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


# Define constant global variables

JSON = "json"
DATA = "data"


class RestError(Exception):
    """
        base module exception to help debug and dev
    """

    def __init__(self, message, session: requests.Session):
        self.message = f"Session {session.headers['Connection']} stopped reason: {message}"
        super().__init__(self.message)


class ParamNotSigned(RestError):
    """
        Error that can happen if you forget to send parameters
        with signed like this -> find_user(id=id) after you config the param in your decorator

    """

    def __init__(self, session, param, arg, func):
        self.msg = f"""param '{param}' is not signed when first call from '{func.__name__}' with '{arg}'
                   consider if you use 'param' argument for our decorators you should
                   call like {func.__name__}({param}={arg})"""
        super().__init__(self.msg, session)


# functions starts here:


class HTTP:
    """
        Holder for some methods
    """

    @staticmethod
    def try_to_json(data):
        """
            try to make a dict if obj is sent
        :param data: obj or dict to send data with request
        :return: data after manipulation or just data
        """
        try:
            return data.__dict__
        except AttributeError:
            return data

    @staticmethod
    def get_response(
            type_: Req,
            ptr__: requests.Session,
            url: str,
            data: [],
            data_t: str
    ) -> requests.Response:
        """
            get the response from request session
        :param type_: type of requests see Req class
        :param ptr__: pointer to object->session
        :param url: link to send request
        :param data: data to send with request
        :param data_t: data type json or data
        :return: response object
        :rtype: requests.Response
        """
        data_temp = json_temp = None
        if data_t == JSON:
            json_temp = data
        else:
            data_temp = data
        return ptr__.request(method=type_.value, url=url, json=json_temp, data=data_temp)

    @staticmethod
    def parse(
            url: str,
            kw: dict,
            param: str,
            self: [],
            args,
            func
    ) -> tuple:
        """
        get all data from the decorator and configure
        how its need to be sent to request
        :rtype:tuple
        """
        data = kw[DATA] if DATA in kw else None
        if data is None: data = args[0] if len(args) != 0 else None
        try:
            param_ = str(kw[param]) if param else ""
        except KeyError:
            raise ParamNotSigned(self._session, param, data, func)
        url_ = self._base_url + url + param_ if url else self._base_url
        data = HTTP.try_to_json(data)
        return data, url_ if (url_.count(param_, 30) > 1 or url) or not url_ else f"{url_}/{param_}"

    @staticmethod
    def request(
            type_: Req,
            url: str = None,
            param: str = None,
            data_t: str = DATA
    ) -> []:
        """
        Decorator with two nasted function to crate the magic function!
        the first function initial the second with same args->
        the second initial the third with same args as well->
        the third runs the first logic-> parse all data params and finally
        crate a request-> the response will update the user defined func\var
        that use this decorator properly-> and then returns user func-> then
        return second and after all of that circle the fist will return
        :param type_: type of requests see Req class
        :param url: link to send request
        :param param: the parameter configuration
        :param data_t: data type json or data
        """

        def decorate(func, **kwargs) -> []:
            def wrapper(self, *args, **kwargs) -> []:
                data, url_ = HTTP.parse(url, kwargs, param, self, args, func)
                self._response = HTTP.get_response(type_, self._session, url_, data, data_t)
                lg.info(f'{func.__name__} -> DATA: {data}\n params: {param} RESPONSE: {self.as_dict()} ')
                return func(self, *args, **kwargs)

            return wrapper

        return decorate


def get(
        url: str = None,
        param: str = None,
        data_t: str = DATA
):
    """
    Create GET request and returns the response
    :param url: url or part of it
    :param param: the user defined parameter name
    :param data_t: type of data default is "data" you can pass "json" too
    :return: response with fun that use this decorator
    :rtype: Any
    """
    return HTTP.request(Req.GET, url, param, data_t)


def delete(
        url: str = None,
        param: str = None,
        data_t: str = DATA
):
    """
        Create DELETE request and returns the response
        :param url: url or part of it
        :param param: the user defined parameter name
        :param data_t: type of data default is "data" you can pass "json" too
        :return: response with fun that use this decorator
        :rtype: Any
        """
    return HTTP.request(Req.DELETE, url, param, data_t)


def post(
        url: str = None,
        param: str = None,
        data_t: str = DATA
):
    """
        Create POST request and returns the response
        :param url: url or part of it
        :param param: the user defined parameter name
        :param data_t: type of data default is "data" you can pass "json" too
        :return: response with fun that use this decorator
        :rtype: Any
    """
    return HTTP.request(Req.POST, url, param, data_t)


def put(
        url: str = None,
        param: str = None,
        data_t: str = DATA
):
    """
        Create PUT request and returns the response
        :param url: url or part of it
        :param param: the user defined parameter name
        :param data_t: type of data default is "data" you can pass "json" too
        :return: response with fun that use this decorator
        :rtype: Any
    """
    return HTTP.request(Req.PUT, url, param, data_t)


#####################################################

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
        lg.info(f"session started... {self._session.headers.items()}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()
        lg.info(f"""session closed.. cookies = {self._session.cookies.items()}
                       auth = {self._session.auth} headers = {self._session.headers.items()}
                         exe_type: {exc_type},exe_val {exc_val}, exe_tb {exc_tb}""")


class Session(SessionContextManager):
    """
        Session Context Manager class
        to make some operations on session

    """
    def __init__(self, headers: [] = ""):
        super().__init__(headers)
        self._headers = headers
        self._login_url: str

    def set_login_url(self, url):
        self._login_url = url

    @property
    def session(self):
        return self._session

    @property
    def headers(self):
        return self._session.headers

    def update_token(self, user, is_created_now=False):
        """
        Update the login user and authorize
        create new users if database are empty
        save the results in file
        :param user: user data to login
        :param is_created_now: true if user are just created and need to store it
        :return: None ot status code
        """
        from commons import utils
        if isinstance(user, str):
            headers = {'Authorization': f'Bearer {user}'}
            self._session.headers.update(headers)
            return
        res = self._session.post(url=self._login_url, json=user['user'])

        if is_created_now:
            user["main_user_id"] = res.json()["userId"]
            user_dict = {"id": res.json()["userId"]}
            utils.write_to_json(user_dict, r"user_id.json")

        try:
            token = res.json()['token']
        except KeyError:
            token = res
        headers = {'Authorization': f'Bearer {token}'}
        self._session.headers.update(headers)
        return res.status_code
