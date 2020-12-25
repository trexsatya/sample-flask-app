from typing import Optional

from marshmallow import post_load, fields, Schema, validates, ValidationError
import datetime as dt

from app.entities.user import User


class UserData:
    def __init__(self, name, email):
        self.id: Optional[int] = None
        self.name = name
        self.email = email

    def __repr__(self):
        return "<User(name={self.name!r})>".format(self=self)

    @staticmethod
    def build_from(user: User):
        if not user:
            return UserData(None, None)
        data = UserData(user.name, user.email)
        data.id = user.id
        data.created_at = user.created_at
        return data


class UserSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    created_at = fields.DateTime()

    @validates("name")
    def validate_quantity(self, name):
        if len(name) > 10:
            raise ValidationError("Name must be less than 50 letters.")

    @post_load
    def make_user(self, data, **kwargs):
        return UserData(**data)
