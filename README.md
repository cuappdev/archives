# fitness-backend

[![Build Status](https://travis-ci.org/cuappdev/fitness-backend.svg?branch=master)](https://travis-ci.org/cuappdev/fitness-backend)

Technologies involved include:
1. Flask
2. SQLAlchemy
3. Marshmallow
4. PostgreSQL

## Setting Up Database
Ensure you have `psql` plus command line tools setup:
````bash
psql postgres
psql> CREATE DATABASE fitnessdb;
mysql> \q
cd src
python manage.py db init  
python manage.py db migrate
python manage.py db upgrade
````

## Virtualenv

Virtualenv setup!

```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pip install git+https://github.com/cuappdev/appdev.py.git --upgrade
```

## Environment Variables
It's recommended to use [`autoenv`](https://github.com/kennethreitz/autoenv).
The required environment variables for this API are the following:

````bash
export DB_USERNAME=CHANGE_ME
export DB_PASSWORD=CHANGE_ME
export DB_HOST=localhost
export DB_NAME=fitnessdb
export APP_SETTINGS=config.CHANGE_ME
````

To source the `.env` file, make a local copy of the `template` file.
`cd` out of the directory, and `cd` back and you should be prompted by `autoenv`.

````bash
cp env.template .env
````
