from flask import Flask
from .config import CONFIG


def create_app(config=None):
    from . import db
    from .views import setup_views

    app = Flask(__name__)
    app.config.from_mapping(CONFIG)

    if config is not None:
        app.config.from_mapping(config)

    db.attach_to_app(app)
    setup_views(app)

    return app

