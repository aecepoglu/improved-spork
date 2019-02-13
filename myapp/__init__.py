from flask import Flask
from .config import CONFIG


def create_app(config=None):
    from . import db

    app = Flask(__name__)
    app.config.from_mapping(CONFIG)

    if config is not None:
        app.config.from_mapping(config)

    db.attach_to_app(app)

    @app.route("/")
    def hello():
        return "The server works."

    return app

