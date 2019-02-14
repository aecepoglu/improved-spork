import click
import json
from pymongo import MongoClient, TEXT as TEXT_INDEX
from flask import current_app, g
from flask.cli import with_appcontext


def get_client():
    if "mongoclient" not in g:
        g.mongoclient = MongoClient(current_app.config["MONGO_URL"])

    return g.mongoclient


def get_db():
    if "db" not in g:
        client = get_client()
        g.db = client.get_default_database()

    return g.db


def close_db(e=None):
    client = g.pop("mongoclient", None)
    _ = g.pop("db", None)

    if client is not None:
        client.close()


def reset_db():
    db = get_db()

    db.drop_collection("songs")

    records_created = 0

    with current_app.open_resource("songs.json") as f:
        for line in f:
            data = json.loads(line)

            db.songs.insert_one(data)
            records_created += 1

    db.songs.create_index([("title", TEXT_INDEX), ("artist", TEXT_INDEX)])

    return {"records_created": records_created}


def attach_to_app(app):
    app.cli.add_command(init_db_command)
    app.teardown_appcontext(close_db)


@click.command("init-db")
@with_appcontext
def init_db_command():
    summary = reset_db()
    click.echo("Initialized the database with {} songs".format(
        summary["records_created"]))
