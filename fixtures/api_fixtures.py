import pytest
from core.api import Services
from core.api import AccountAPI
from core.api import BookAPI
from core.api import AuthorsAPI
from core.api.constant import *
from commons import json_read
from commons import RandomData
from core.models import LoginDto
from core.models import ApiUserDto
from core.api import session as se
from core.api.constant import ENDPOINTS
from commons.utils import log_data


@pytest.fixture(scope="session")
def data():
    return RandomData()


@pytest.fixture(scope="session")
def fix_user():
    user = json_read(r"data_api.json")
    user_id = json_read(r"user_id.json")
    return {"user": ApiUserDto(**user['main_user']), "userid": user_id['id']}


@pytest.fixture(scope="session")
def fix_admin_user():
    user = json_read(r"data_api.json")
    return LoginDto(**user['admin'])


@pytest.fixture(scope="session")
def bearer_au_session(fix_user, fix_admin_user, configuration) -> se.Session:
    user_dict = {"user": fix_user['user'].to_json(), "main_user_id": fix_user['userid']}
    with se.Session() as new_session:
        new_session.session.post(url=f"{configuration.url[:-1]}{URL_SWAGGER}{ACCOUNT_URL}/register", json=ApiUserDto(
            fix_admin_user.email, fix_admin_user.password, "admin", "admin").to_json())
        new_session.set_login_url(f'{configuration.url[:-1]}{URL_SWAGGER}{ACCOUNT_URL}/login')
        code = new_session.update_token(user_dict)
        if code == 401:
            new_session.session.post(f'{configuration.url[:-1]}{URL_SWAGGER}{ACCOUNT_URL}/register',
                                     json=user_dict['user'])
            new_session.update_token(user_dict, True)
        yield new_session


@pytest.fixture(scope="session")
def api(bearer_au_session, configuration) -> Services:
    session = bearer_au_session
    api = Services()
    services = {"_books_": BookAPI, "_account_": AccountAPI, "_authors_": AuthorsAPI}
    for name, service in services.items():
        api[name] = service(f"{configuration.url[:-1]}{ENDPOINTS[name]}", session)
    api._session_ = session
    log_data(str(api))
    return api
