import pytest

from webtest import TestApp

from app.main import create_app


class TestConfig:
    pass


@pytest.fixture(scope='function')
# scope='function' means that this object would be created when it is required by test function,
# and will be destroyed when the function completes (i.e. fixture goes out of scope)
def app():
    """An application for running tests"""
    _app = create_app(TestConfig)

    with _app.app_context():
        pass

    ctx = _app.test_request_context()
    ctx.push()

    yield _app
    # Below is the tear-down code run after the fixture goes out of scope
    ctx.pop()


@pytest.fixture(scope='function')
def testapp(app):
    """A Webtest app."""
    return TestApp(app)
