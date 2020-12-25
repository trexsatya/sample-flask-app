import traceback

import transaction
from flask import Flask, url_for
from flask_injector import FlaskInjector
from injector import singleton

from app.controllers.static_controller import static_blueprint
from app.controllers.user_controller import user_blueprint
from app.extensions import database, migrate
from app.services.user import ExternalService, UserService


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


def create_app(config_object):
    _app = Flask(__name__.split(".")[0])
    _app.config.from_object(config_object)
    _app.register_blueprint(user_blueprint)
    _app.register_blueprint(static_blueprint)

    def configure_di(binder):
        binder.bind(ExternalService, to=ExternalService, scope=singleton)
        binder.bind(UserService, to=UserService, scope=singleton)

    FlaskInjector(app=_app, modules=[configure_di])
    database.init_app(_app)
    migrate.init_app(_app, db=database)

    _app.errorhandler(Exception)(generic_error_handler)
    return _app
