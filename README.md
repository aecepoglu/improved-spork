# A Backend in Python

An API defining the routes listed below.

Requirements:

- Use python with Flask.
- Use a MongoDB server for storing the data provided in the file `songs.json`.
- All routes should return a valid json dictionary.
- Write tests for the API.
- Follow the KISS principle.
- Provide all instructions to do the setup, the easier it is for us to get it running the better. 
- Please take into consideration that the number of songs and ratings will grow to millions of documents as well as the number of users using the API.

List of routes:

- `GET /songs`
  - Returns a list of songs with some details on them
  - Add possibility to paginate songs.
- `GET /songs/avg/difficulty`
  - Takes an optional parameter `level` to select only songs from a specific level.
  - Returns the average difficulty for all songs.
- `GET /songs/search`
  - Takes in parameter a 'message' string to search.
  - Return a list of songs. The search should take into account song's artist and title. The search should be case insensitive.
- `POST /songs/rating`
  - Takes in parameter a `song_id` and a `rating`
  - This call adds a rating to the song. Ratings should be between 1 and 5.
- `GET /songs/avg/rating/<song_id>`
  - Returns the average, the lowest and the highest rating of the given song id.

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
