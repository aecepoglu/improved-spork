local_db = {
    1: "yes",
    2: "no",
    3: "maybe",
}


def find(_id):
    if _id in local_db:
        return local_db[_id]
    else:
        return "Not Found"


def add(_id, value):
    global local_db
    local_db[_id] = value
    return value


def list():
    return [(k, v) for (k, v) in local_db.items()]
