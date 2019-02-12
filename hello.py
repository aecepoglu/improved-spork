from flask import Flask
import db

app = Flask(__name__)


@app.route("/words/<int:word_id>")
def show_word_at_id(word_id):
    return db.find(word_id)


@app.route("/words/<int:word_id>", methods=["PUT"])
def update_word_at_id(word_id):
    return db.add(word_id, request.form["word"])


@app.route("/words")
def list_words():
    return ", ".join(["({}, {})".format(k, v) for (k, v) in db.list()])


@app.route("/")
def hello():
    return "Hello World!"
