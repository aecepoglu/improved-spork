# aec's yousician assignment
---------------------------

## Install & Run using Docker

    docker-compose up --build
    # open the same directory in a different terminal
    docker-compose run myapi init-db
    # it should now be available at http://localhost:5000

## Install & Run Locally

1. (optionally) setup a virtual environment

        mkdir aecs-env
        python -m venv aecs-env
        source aecs-env/bin/activate

1. Install dependencies

        pip install -r requirements.txt

1. Configure

        cp .env.default .env
        source .env

    See [configuration](#Configuration) for options

1. Run

        flask init-db
        flask run
        # it should now be available at http://localhost:5000

    [more info at Flask CLI](http://flask.pocoo.org/docs/1.0/cli/)


## Run Tests

All tests are defined in `features/**/*.feature`

Test all features with:

    export MONGO_TEST_URL="mongodb://your-mongo:27017/your-test-db"
    behave


## Configuration

* `MONGO_URL`: the mongo url "mongodb://localhost:27017/my-database"
* `MONGO_TEST_URL`: the mongo url to use in tests "mongodb://localhost/27017/my-test-db"
* `FLASK_RUN_PORT`: defaults to 5000

## Development

* lint your code with `pycodestyle myapp/*.py`

## Helpful Links

* [Creating and using virtual envs](https://packaging.python.org/tutorials/installing-packages/#id16)
