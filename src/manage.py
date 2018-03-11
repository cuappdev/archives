import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db
from scripts import scraper

# Build manager
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def scrape():
  scraper.update_db(10) # number of pages to scrape

if __name__ == '__main__':
  manager.run()
