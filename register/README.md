# Register

Logging for all of our apps `:)`

## Installing
Make sure you have `virtualenv` installed.
On creating a `virtualenv` called `venv`, run the following:

```bash
pip install git+https://github.com/cuappdev/appdev.py.git#egg=appdev.py
pip install -r requirements.txt
```

## Setting Up Database
Ensure you have `psql` plus command line tools setup:
```bash
psql
psql> CREATE DATABASE my_db_name;
psql> \q
cd src/scripts
python setup_db.py
```

## Environment Variables
I highly recommend [`autoenv`](https://github.com/kennethreitz/autoenv).
The required environment variables for this API are the following:

```bash
export DB_USERNAME=CHANGE_ME
export DB_PASSWORD=CHANGE_ME
export DB_HOST=localhost
export DB_NAME=my_db_name
export APP_SETTINGS=config.CHANGE_ME
```

## Frontend Development

To start working on frontend, follow the following instructions:
1. In one terminal window, run `python src/run.py`
2. In a second terminal window, run `cd src/client && npm run dev` (`webpack-dev-server`)
3. Open up `localhost:8080` - any changes to files will live-reload your site

## Testing
To run all unit tests, from the `/tests` directory, run:

```bash
./test.sh
```

To run a single test, from the `/tests` directory, run:

```bash
./test.sh test_file_name.py
```
