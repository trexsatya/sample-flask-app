import pytest

from webtest import TestApp

from app.extensions import database
from app.main import create_app


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


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


@pytest.fixture(scope="function")
def db(app):
    # By this fixture, we'll have a clean DB for each test method.
    database.app = app
    with app.app_context():
        database.create_all()

    yield database

    database.session.close()
    database.drop_all()
