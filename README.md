# Cornell App Development Website

[Check it out!](http://www.cornellappdev.com/)

## How to Contribute

You must set up `Rails` to work with this project.  To install `Rails`, follow the guide [`here`](http://railsapps.github.io/installrubyonrails-mac.html).

You should also have `PostgreSQL` installed.  Install it [`here`](https://postgresapp.com/).  

Run the following to setup the project:

```
bundle install
bundle exec rake db:create
bundle exec rake db:migrate
```

To run the server:

```
rails s
```

## How to Deploy with Heroku

Create a remote for the existing Heroku app:

```
heroku git:remote -a appdev-site
```

Deploy the site:

```
git push heroku master
```
