from flask import jsonify, Blueprint, request
from flask.views import MethodView
from flask_apispec import marshal_with
from flaskext.auth import login_required
from injector import inject

from app.dto.user import UserSchema, UserData
from app.entities.user import User
from app.extensions import database, auth
from app.services.user_service import UserService
from app.utils import validate_with, ensure_resource_present

user_blueprint = Blueprint("users_api", __name__)


user_schema = UserSchema()


class UserController(MethodView):
    @inject
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    @marshal_with(UserSchema(many=True))
    @auth.login_required()
    def get(self, user_id):
        if user_id is not None:
            user = User.find_first(id=user_id)
            ensure_resource_present(user)
            return [UserData.build_from(user)]
        else:
            users = User.find_all()
            ensure_resource_present(users)
            print("users", )
            return list(map(lambda x: UserData.build_from(x), users))

    @marshal_with(UserSchema(many=False))
    @auth.login_required(role="admin")
    def post(self):
        validate_with(user_schema)
        user_data: UserData = user_schema.load(request.get_json())
        user = self.user_service.create_user(user_data)
        return UserData.build_from(user)


user_view = UserController.as_view("api")
user_blueprint.add_url_rule(
        "/api/v1/users", defaults={"user_id": None}, view_func=user_view, methods=["GET"]
)
user_blueprint.add_url_rule("/api/v1/users/<int:user_id>", view_func=user_view, methods=["GET"])
user_blueprint.add_url_rule("/api/v1/users", view_func=user_view, methods=["POST"])
