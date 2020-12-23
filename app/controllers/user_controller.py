from flask import jsonify, Blueprint
from flask.views import MethodView

FAKE_DATA = [{"user_id": 1, "value": "duck"}, {"user_id": 2, "value": "cat"}]

user_blueprint = Blueprint("users_api", __name__)


class UserController(MethodView):
    def get(self, user_id):
        if user_id is None:
            return jsonify(FAKE_DATA)
        else:
            return jsonify(list(filter(lambda x: x['user_id'] == user_id, FAKE_DATA)))


user_view = UserController.as_view("api")
user_blueprint.add_url_rule(
        "/api/v1/users", defaults={"user_id": None}, view_func=user_view, methods=["GET"]
)
user_blueprint.add_url_rule("/api/v1/users/<int:user_id>", view_func=user_view, methods=["GET"])
