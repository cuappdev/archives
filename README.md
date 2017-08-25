# Tempo API

The required environment variables for this API are the following:

````bash
DB_USERNAME
DB_PASSWORD
DB_HOST
DB_NAME
APP_SETTINGS
SPOTIFY_REDIRECT_URI
SPOTIFY_CLIENT_ID
SPOTIFY_SECRET
TEMPO_REDIRECT
````

The following workflow to migrate your database is the following:

````bash
cd src
python manage.py db init # only the first time
python manage.py db migrate
python manage.py db upgrade
````

To run the app:

````bash
python src/run.py
````
