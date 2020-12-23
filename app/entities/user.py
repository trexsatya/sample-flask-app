from sqlalchemy import String, Integer
import datetime as dt
from app.extensions import database


class User(database.Model):
    __tablename__ = "users"
    id = database.Column(Integer, primary_key=True)
    name = database.Column(String(10), nullable=False)
    email = database.Column(String(50), nullable=False)

    created_at = database.Column(database.DateTime, nullable=False, default=dt.datetime.utcnow)
    updated_at = database.Column(database.DateTime, nullable=False, default=dt.datetime.utcnow)

    def __init__(self, **kwargs):
        database.Model.__init__(self, **kwargs)