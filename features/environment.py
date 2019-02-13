from os import getenv
from behave import use_fixture
from myapp import create_app
from myapp.db import attach_to_app, reset_db


def before_feature(context, feature):
    print("creating the app...")
    app = create_app({
        "MONGO_URL": getenv("MONGO_TEST_URL", "mongodb://localhost:27017")
        })

    context.client = app.test_client()

    with app.app_context():
        reset_db()
        attach_to_app(app)
