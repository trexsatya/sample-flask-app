from flask import send_from_directory, current_app, Blueprint, config
import os

static_blueprint = Blueprint("static_data", __name__)


def favicon():
    return send_from_directory(current_app.config["PROJECT_ROOT"],
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


static_blueprint.add_url_rule("/favicon.ico", view_func=favicon, methods=["GET"])
