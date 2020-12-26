from json import loads

from flask import Blueprint, request, jsonify
from flask_apispec import marshal_with
from injector import inject
from marshmallow import fields, Schema
from requests import get

from app.dto.user import UserData, UserSchema
from app.entities.user import User
from app.exceptions import AuthException
from app.services.auth_service import AuthService
from app.services.google_service import GoogleService
from app.services.user_service import UserService

auth_blueprint = Blueprint("auth_api", __name__)


@auth_blueprint.route("/api/v1/auth/login", methods=["POST"])
# @marshal_with(UserSchema())
def google_login():
    req = request.get_json()
    if req['social'] != 'google':
        return {"message": "Not supported"}, 400
    token_result = GoogleService.get_token_info(req['idToken'])

    user = User.find_first(email=token_result['email'])
    if not user:
        raise AuthException("User not registered")

    return jsonify({"access_token": AuthService.create_token(user)})


@auth_blueprint.route("/api/v1/auth/register", methods=["POST"])
@marshal_with(UserSchema())
@inject
def google_register(user_service: UserService):
    req = request.get_json()
    if req['social'] != 'google':
        return {"message": "Not supported"}, 400
    token_result = GoogleService.get_token_info(req['idToken'])
    user = user_service.create_user(UserData(name=token_result['given_name'] + " " + token_result['family_name'],
                                             email=token_result['email'],
                                             email_verified=(True if
                                                             token_result['email_verified'] or
                                                             token_result['email_verified'] == 'true'
                                                             else False)
                                             )
                                    )
    return UserData.build_from(user)
