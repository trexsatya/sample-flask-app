from flask import Flask

from app.controllers.user_controller import user_blueprint


def create_app(config_object):
    _app = Flask(__name__.split(".")[0])
    _app.config.from_object(config_object)
    _app.register_blueprint(user_blueprint)
    return _app