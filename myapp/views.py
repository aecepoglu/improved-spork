from flask import request
from .db import get_db
from json import JSONEncoder
from bson import ObjectId


class MyJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return JSONEncoder.default(self, o)


jsonify = MyJSONEncoder().encode


class BadRequestException(Exception):
    def __init__(self, msg):
        Exception.__init__(self)
        self.message = msg


def setup_views(app):
    @app.errorhandler(BadRequestException)
    def handle_bad_request_error(err):
        return err.message, 400

    @app.route("/")
    def hello():
        return "The server works."

    @app.route("/songs")
    def list_songs_route():
        offset = request.args.get("offset", 0, type=int)
        pagesize = request.args.get("pagesize", 20, type=int)

        db = get_db()

        total_count = db.songs.count_documents({})
        cursor = db.songs.find({}, {
            "artist": 1,
            "title": 1
        }).skip(offset).limit(pagesize)

        results = [x for x in cursor]

        return jsonify({
            "offset": offset,
            "pagesize": pagesize,
            "cur_count": len(results),
            "total_count": total_count,
            "results": results
        })

    @app.route("/songs/search")
    def search_songs_route():
        offset = request.args.get("offset", 0, type=int)
        pagesize = request.args.get("pagesize", 20, type=int)
        message = request.args.get("message", "", type=str)
        print("MESSAGE: " + message)

        db = get_db()
        query_filter = {}

        if message is not "":
            query_filter = {"$text": {"$search": "\"{}\"".format(message)}}

        total_count = db.songs.count_documents(query_filter)
        cursor = db.songs.find(query_filter, {
            "artist": 1,
            "title": 1
        }).skip(offset).limit(pagesize)

        results = [x for x in cursor]

        return jsonify({
            "offset": offset,
            "pagesize": pagesize,
            "cur_count": len(results),
            "total_count": total_count,
            "results": results
        })

    @app.route("/songs/avg/difficulty")
    def avg_difficulty_route():
        level = request.args.get("level", type=int)
        query_filters = {}

        if "level" in request.args:
            query_filters["level"] = int(request.args["level"])

        db = get_db()
        cursor = db.songs.aggregate([{
            "$match": query_filters
        }, {
            "$group": {
                "_id": None,
                "avg": {
                    "$avg": "$difficulty"
                }
            }
        }])

        results = [{"average_difficulty": round(x["avg"], 2)} for x in cursor]

        if len(results) == 0:
            raise BadRequestException(
                "avg difficulty couldn't be calculated for {}".format(
                    ", ".join([
                        "{}: {}".format(k, v)
                        for k, v in query_filters.items()
                    ])))

        return jsonify(results[0])
