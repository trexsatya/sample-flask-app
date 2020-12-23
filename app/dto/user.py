from marshmallow import post_load, fields, Schema, validates, ValidationError
import datetime as dt


class UserData:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.created_at = dt.datetime.now()

    def __repr__(self):
        return "<User(name={self.name!r})>".format(self=self)


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
