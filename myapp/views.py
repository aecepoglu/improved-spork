from flask import request, Response
from .db import get_db
from json import JSONEncoder
from bson import ObjectId
from pymongo import ReturnDocument


class MyJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return JSONEncoder.default(self, o)


jsonify = MyJSONEncoder().encode


def json_response(x):
    return Response(jsonify(x), mimetype="application/json")


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

        return json_response({
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

        return json_response({
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

        return json_response(results[0])

    @app.route("/songs/rating", methods=["POST"])
    def add_rating_route():
        if "song_id" not in request.args:
            raise BadRequestException("'song_id' is required")
        if "rating" not in request.args:
            raise BadRequestException("'rating' is required")

        song_id = request.args.get("song_id", type=str)
        rating = request.args.get("rating", type=int)

        if rating > 5:
            raise BadRequestException(
                "Rating too high. Must be between 1 and 5.")
        if rating <= 0:
            raise BadRequestException(
                "Rating too low. Must be between 1 and 5.")

        db = get_db()
        query = {"_id": ObjectId(song_id)}

        song = db.songs.find_one(query)

        if song is None:
            raise BadRequestException("No such song")

        info = song["ratings"] if "ratings" in song else {
            "num_ratings": 0,
            "max_rating": 0,
            "min_rating": 5,
            "avg_rating": 0
        }

        updated_song = db.songs.find_one_and_update(
            query, {
                "$set": {
                    "ratings": {
                        "num_ratings":
                        info["num_ratings"] + 1,
                        "max_rating":
                        max(rating, info["max_rating"]),
                        "min_rating":
                        min(rating, info["min_rating"]),
                        "avg_rating":
                        round(((info["num_ratings"] * info["avg_rating"]) +
                               rating) / (info["num_ratings"] + 1), 1)
                    }
                }
            },
            return_document=ReturnDocument.AFTER)

        return json_response(updated_song["ratings"])

    @app.route("/songs/avg/rating")
    def show_ratings_route():
        if "song_id" not in request.args:
            raise BadRequestException("'song_id' is required")

        song_id = request.args.get("song_id", type=str)
        db = get_db()
        query = {"_id": ObjectId(song_id)}

        song = db.songs.find_one(query)

        if song is None:
            raise BadRequestException("No such song")

        info = song["ratings"] if "ratings" in song else {
            "num_ratings": 0,
            "max_rating": 0,
            "min_rating": 0,
            "avg_rating": 0
        }

        return json_response(info)
