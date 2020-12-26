from flask import request

from app.entities.user import User
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import os
from datetime import timedelta

from app.extensions import auth

token_serializer = Serializer(os.getenv("SECRET_KEY"), expires_in=3600, algorithm_name="HS256")


class AuthService:
    @staticmethod
    def verify_token(token):
        try:
            data = token_serializer.loads(token)
        except Exception as e:
            print("verify_token():", token, e, request.headers)
            return False
        return data

    @staticmethod
    def create_token(user: User):
        payload = {"email": user.email, "name": user.name, "roles": ["user"]}
        print("payload", payload)
        return token_serializer.dumps(payload).decode('utf-8')


@auth.verify_token
def verify_token(token):
    return AuthService.verify_token(token)


@auth.get_user_roles
def get_user_roles(user):
    print("get_user_roles", user)
    return user["roles"]







