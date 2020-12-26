import traceback

import transaction
from flask import Flask, url_for
from flask_injector import FlaskInjector
from flaskext.auth import Auth
from injector import singleton

from app.controllers.auth_controller import auth_blueprint
from app.controllers.static_controller import static_blueprint
from app.controllers.user_controller import user_blueprint
from app.exceptions import AuthException
from app.extensions import database, migrate, auth
from app.services.auth_service import AuthService
from app.services.user_service import ExternalService, UserService


def generic_error_handler(exception):
    """
    This will handle all uncaught exceptions while Flask is processing a request.
    :param exception:
    :return:
    """
    # database.session.rollback()
    transaction.abort()
    trace = "\n".join(traceback.format_exception(etype=type(exception), value=exception, tb=exception.__traceback__))
    print(trace)
    return {"message": "Error"}, 500


def auth_exception_handler(exception: Exception):
    trace = "\n".join(traceback.format_exception(etype=type(exception), value=exception, tb=exception.__traceback__))
    print(trace)
    return {"message": getattr(exception, 'message', repr(exception)) }, 401


def create_app(config_object):
    _app = Flask(__name__.split(".")[0])
    _app.config.from_object(config_object)
    _app.register_blueprint(user_blueprint)
    _app.register_blueprint(static_blueprint)
    _app.register_blueprint(auth_blueprint)

    def configure_di(binder):
        binder.bind(ExternalService, to=ExternalService, scope=singleton)
        binder.bind(UserService, to=UserService, scope=singleton)

    FlaskInjector(app=_app, modules=[configure_di])
    database.init_app(_app)
    migrate.init_app(_app, db=database)

    auth = Auth(_app)

    _app.errorhandler(AuthException)(auth_exception_handler)
    _app.errorhandler(Exception)(generic_error_handler)
    return _app
