from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy, Model
import datetime as dt
from zope.sqlalchemy import register
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# from app.services.auth_service import AuthService


class CRUDMixin(Model):
    """Mixin that adds convenience methods for CRUD (Create, Read, Update, Delete) operations"""
    @classmethod
    def find_all(cls, **kwargs):
        return cls.query.filter_by(**kwargs).all()

    @classmethod
    def find_first(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    def save(self, commit=True):
        database.session.add(self)
        if commit:
            database.session.commit()
        return self

    def update(self, commit=True, **kwargs):
        self.updated_at = dt.datetime.utcnow()
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def delete(self, commit=True):
        database.session.delete(self)
        return commit and database.session.commit()


database = SQLAlchemy(model_class=CRUDMixin, session_options={"expire_on_commit": False})
register(database.session)
migrate = Migrate()
auth = HTTPTokenAuth('Bearer')

