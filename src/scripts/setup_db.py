import sys
import os
import shutil
import datetime as dt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.dao import gyms_dao as gd
from app.dao import gymhours_dao as ghd

def setup_dbs():
  print 'Setting up databases...'
  os.chdir('..')
  os.system('python manage.py db init')
  os.system('python manage.py db migrate')
  os.system('python manage.py db upgrade')
  os.chdir('scripts')
  print 'Finished setting up databases...'

def delete_migrations():
  try:
    os.chdir('..')
    shutil.rmtree('migrations')
    os.system('mysql --user={} --password={} --host={} {} '
              .format(os.environ['DB_USERNAME'], os.environ['DB_PASSWORD'],
                      os.environ['DB_HOST'], os.environ['DB_NAME'])
              + '--execute "drop table alembic_version"')
    os.chdir('scripts')
    print 'Migrations folder deleted...'

    # adding gyms to db
    print 'Adding gyms to db...'
    _, helen_newman = gd.create_gym("Helen Newman", is_gym=True)
    _, teagle_up = gd.create_gym("Teagle Up", is_gym=True)
    _, teagle_down = gd.create_gym("Teagle Down", is_gym=True)
    _, noyes = gd.create_gym("Noyes", is_gym=True)
    _, appel = gd.create_gym("Appel", is_gym=True)

    # adding gym_hours to db
    print 'Adding gym_hours to db...'
    # helen_newman
    ghd.create_gym_hour(helen_newman.id, 0, dt.time(10), dt.time(23, 30))
    for n in range(1, 5):
        ghd.create_gym_hour(helen_newman.id, n, dt.time(6), dt.time(23, 30))
    ghd.create_gym_hour(helen_newman.id, 6, dt.time(10), dt.time(22))
    # teagle_up
    ghd.create_gym_hour(teagle_up.id, 0, dt.time(12), dt.time(17, 45))
    for n in range(1, 4):
        ghd.create_gym_hour(teagle_up.id, n, dt.time(7), dt.time(22, 45))
    ghd.create_gym_hour(teagle_up.id, 5, dt.time(7), dt.time(20))
    ghd.create_gym_hour(teagle_up.id, 6, dt.time(12), dt.time(17, 45))
    # teagle_down
    ghd.create_gym_hour(teagle_down.id, 0, dt.time(12), dt.time(17, 45))
    for n in range(1, 4):
        ghd.create_gym_hour(teagle_down.id, n, dt.time(7), dt.time(22, 45))
    ghd.create_gym_hour(teagle_down.id, 5, dt.time(7), dt.time(20))
    ghd.create_gym_hour(teagle_down.id, 6, dt.time(12), dt.time(17, 45))
    # noyes
    ghd.create_gym_hour(noyes.id, 0, dt.time(11, 30), dt.time(23, 30))
    for n in range(1, 5):
        ghd.create_gym_hour(noyes.id, n, dt.time(7), dt.time(23, 30))
    ghd.create_gym_hour(noyes.id, 6, dt.time(11, 30), dt.time(22))
    # appel
    ghd.create_gym_hour(appel.id, 0, dt.time(9), dt.time(13))
    for n in range(1, 5):
        ghd.create_gym_hour(appel.id, n, dt.time(15), dt.time(23, 30))
    ghd.create_gym_hour(appel.id, 6, dt.time(9), dt.time(13))


  except OSError:
    os.chdir('scripts')
    print 'No migrations folder to delete...'

if __name__ == '__main__':
  delete_migrations()
  setup_dbs()
