# Podcast ML Service

## Virtual Environment

Make sure you have [`virtualenv`](https://virtualenv.pypa.io/en/stable/) installed.  
On creating a `virtualenv` and activating it, run the following:

````bash
pip install git+https://github.com/cuappdev/appdev.py.git#egg=appdev.py
pip install -r requirements.txt
````

## Setting up Database

Ensure you have `mysql` plus command line tools setup.  Then run the following.  It creates
databases, migrates them, and loads in necessary `dev` / `test` data:

````bash
./setup.sh
````

If the `migrations` directory is ever deleted, you can regenerate it with the following:

````bash
python manage.py db init --multidb
````

## Environment Variables

I highly recommend [`autoenv`](https://github.com/kennethreitz/autoenv).
The required environment variables for this API are the following:

````bash
API_KEY
DB_USERNAME
DB_PASSWORD
DB_HOST
DB_NAME
TEST_DB_USERNAME
TEST_DB_PASSWORD
TEST_DB_HOST
TEST_DB_NAME
APP_SETTINGS # e.g. config.DevelopmentConfig
````

If using `autoenv` for local development, create a `.env` file, like the sample below:
````bash
export API_KEY=CHANGEME
export DB_USERNAME=CHANGEME
export DB_PASSWORD=CHANGEME
export DB_HOST=localhost
export DB_NAME=pcasts_ml_db_dev
export TEST_DB_USERNAME=CHANGEME
export TEST_DB_PASSWORD=CHANGEME
export TEST_DB_HOST=localhost
export TEST_DB_NAME=test_pcasts_ml_db_dev
export APP_SETTINGS=config.DevelopmentConfig
````


In the `/tests` directory, create another `.env` file that changes the `APP_SETTINGS`:
````bash
export APP_SETTINGS=config.TestingConfig
````

## Testing
To run all unit tests, from the `/tests` directory, run:
````
nosetests
````

To run a single test, from the `/tests` directory, run:
````
nosetests test_file_name.py
````
