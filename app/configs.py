import os

from dotenv import load_dotenv

load_dotenv()
# This will load .env file containing environment variables


class Config(object):
    """Base Configuration"""
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))


class ProdConfig(Config):
    ENV = 'prod'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URL")


class DevConfig(Config):
    ENV = 'dev'
    DEBUG = True
    DB_NAME = 'dev.db'
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_URL',
                                        'sqlite:///{0}'.format(DB_PATH)  # default
                                        )
    print("satya", SQLALCHEMY_DATABASE_URI)
