# Podcast App Web Client 

[Cornell App Development](http://www.cuappdev.org) Podcast HTTP client.  

## PostgreSQL Database Setup 

This client requires three environment variables, `PSQL_URL`, `PSQL_USER`, `PSQL_PASSWORD`.  Having these present for both development and production environments is useful, this way only environment variables need to be changed with out any config-file modifications.  

When developing, it is recommended that you create a **PostgreSQL** user that is specific for app development.  You can do so by running the following as the Super User in the `psql` terminal: 

```
CREATE USER my_user with password 'my_password'; 
```

To create the DB for this project, run the following: 

```
CREATE DATABASE podcast_web_dev;
```

In order to maintain environment variables specific to a project, you can package into this directory a `.env` file with the environment variables you'd like to include.  This, combined with the [`autoenv`](https://github.com/kennethreitz/autoenv) tool makes environment-variable-loading a breeze.

The `.env` file should follow the a specific format w/regards to the Postgres database: 

```
export PSQL_URL="jdbc:postgresql://localhost:5432/podcast_web_dev"
export PSQL_USER="my_user"
export PSQL_PASSWORD="my_password"
```

Note the `jdbc` at the beginning of the postgres database URL.


