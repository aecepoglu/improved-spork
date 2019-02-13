from os import environ


def getenv_or_cry(name):
    if name in environ:
        return environ[name]
    else:
        raise Exception("The env variable '{}' is required.".format(name))


CONFIG = {
    "MONGO_URL": getenv_or_cry("MONGO_URL"),
}
