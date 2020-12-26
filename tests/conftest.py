import pytest
from flask_httpauth import HTTPAuth

from webtest import TestApp

from app.extensions import database
from app.main import create_app


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def fake_verify_token(token):
    print("fake_verify_token", token)
    if not token:
        return None
    roles = ["user"]
    if "admin" in token:
        roles = ["admin"]
    return {"roles": roles, "email": "fake@mail.com"}


def as_admin():
    return {"headers": {"Authorization": "Bearer admin"}}


def as_user():
    return {"headers": {"Authorization": "Bearer user"}}


@pytest.fixture(scope='function')
# scope='function' means that this object would be created when it is required by test function,
# and will be destroyed when the function completes (i.e. fixture goes out of scope)
def app(monkeypatch):
    """An application for running tests"""
    _app = create_app(TestConfig)
    _app.config['LOGIN_DISABLED'] = True  # Not working

    monkeypatch.setattr("app.services.auth_service.AuthService.verify_token", fake_verify_token)

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


def raise_exception(exc):
    raise exc
