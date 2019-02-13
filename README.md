# aec's yousician assignment
---------------------------

TODO explanation (and possibly link to the main assignment)

## Install & Run using Docker

    docker-compose up --build

## Install & Run Locally

1. (optionally) setup a virtual environment

        mkdir aecs-env
        python -m venv aecs-env

2. Install dependencies

        pip install -r requirements.txt

3. Run

        FLASK_APP=hello flask run

    [more info at Flask CLI](http://flask.pocoo.org/docs/1.0/cli/)


## Run Tests

The tests are available in `features/**/*.feature`

Run with:

    behave


## Configuration

* `MONGO_URL`: for example: "mongodb://localhost:27017/my-database"
* `MONGO_TEST_URL`: for example: "mongodb://localhost/27017/my-test-db"
* `FLASK_RUN_PORT`: defaults to 5000

TODO (configuration is available at Dockerfile)

## Development

* lint your code with `pycodestyle *.py`

## Helpful Links

* [Creating and using virtual envs](https://packaging.python.org/tutorials/installing-packages/#id16)
