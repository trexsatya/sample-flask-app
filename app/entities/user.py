from sqlalchemy import String, Integer, Boolean
import datetime as dt
from app.extensions import database


class User(database.Model):
    __tablename__ = "users"
    id = database.Column(Integer, primary_key=True)
    name = database.Column(String(10), nullable=False)
    email = database.Column(String(50), nullable=False, unique=True)
    email_verified = database.Column(Boolean(), nullable=False, default=False)
    account_suspended = database.Column(Boolean(), nullable=False, default=False)
    social_login = database.Column(String(50), nullable=True)
    created_at = database.Column(database.DateTime, nullable=False, default=dt.datetime.utcnow)
    updated_at = database.Column(database.DateTime, nullable=False, default=dt.datetime.utcnow)

    def __init__(self, **kwargs):
        database.Model.__init__(self, **kwargs)