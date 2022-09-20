from fixtures import *


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


def pytest_addoption(parser):
    data = TestsData.load(DATA_FILE)
    parser.addoption("--url", action="store", default=data.url)
    parser.addoption("--lib", action="store", default=data.lib)
    parser.addoption("--browser", action="store", default=data.browser)
    parser.addoption("--grid", action="store", default=data.selenium_grid)
