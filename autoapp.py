from flask.helpers import get_debug_flag

from app.configs import DevConfig, ProdConfig
from app.main import create_app

CONFIG = DevConfig if get_debug_flag() else ProdConfig

app = create_app(CONFIG)
