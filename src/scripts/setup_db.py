import sys
import os
import shutil
import datetime as dt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.dao import class_descs_dao as cdd
from app.dao import class_tags_dao as ctd
from app.dao import gyms_dao as gd
from app.dao import gymhours_dao as ghd
from app.models.populartimeslist import PopularTimesList as Ptl
from app.utils import db_utils

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
    os.system('export PGPASSWORD={}; psql --user={} --host={} {} '
              .format(os.environ['DB_PASSWORD'], os.environ['DB_USERNAME'],
                      os.environ['DB_HOST'], os.environ['DB_NAME'])
              + '-c "drop table alembic_version"')
    os.chdir('scripts')
    print 'Migrations folder deleted...'

  except OSError:
    os.chdir('scripts')
    print 'No migrations folder to delete...'

def init_data():
    # adding gyms to db
    print 'Adding gyms to db...'

    image_prefix = "https://raw.githubusercontent.com/cuappdev/" + \
        "assets/master/fitness/"
    _, helen_newman = gd.create_gym(
        "Helen Newman",
        image_url=image_prefix + "gyms/Helen_Newman.jpg",
        is_gym=True
    )
    _, teagle_up = gd.create_gym(
        "Teagle Up",
        image_url=image_prefix + "gyms/Teagle.jpg",
        is_gym=True
    )
    _, teagle_down = gd.create_gym(
        "Teagle Down",
        image_url=image_prefix + "gyms/Teagle.jpg",
        is_gym=True
    )
    _, noyes = gd.create_gym(
        "Noyes",
        image_url=image_prefix + "gyms/Noyes.jpg",
        is_gym=True
    )
    _, appel = gd.create_gym(
        "Appel",
        image_url=image_prefix + "gyms/Appel.jpg",
        is_gym=True
    )
    _, bartel = gd.create_gym(
        "Bartels",
        image_url=image_prefix + "gyms/Noyes.jpg",
        is_gym=True
    )

    # adding gym_hours to db
    print 'Adding gym_hours to db...'
    # helen_newman
    ghd.create_gym_hour(helen_newman.id, 0, dt.time(10), dt.time(23, 30))
    for n in range(1, 6):
      ghd.create_gym_hour(helen_newman.id, n, dt.time(6), dt.time(23, 30))
    ghd.create_gym_hour(helen_newman.id, 6, dt.time(10), dt.time(22))

    # teagle_up
    ghd.create_gym_hour(teagle_up.id, 0, dt.time(12), dt.time(17, 45))
    for n in range(1, 5):
      ghd.create_gym_hour(teagle_up.id, n, dt.time(7), dt.time(22, 45))
    ghd.create_gym_hour(teagle_up.id, 5, dt.time(7), dt.time(20))
    ghd.create_gym_hour(teagle_up.id, 6, dt.time(12), dt.time(17, 45))

    # teagle_down
    ghd.create_gym_hour(teagle_down.id, 0, dt.time(12), dt.time(17, 45))
    for n in range(1, 5):
      ghd.create_gym_hour(teagle_down.id, n, dt.time(7), dt.time(22, 45))
    ghd.create_gym_hour(teagle_down.id, 5, dt.time(7), dt.time(20))
    ghd.create_gym_hour(teagle_down.id, 6, dt.time(12), dt.time(17, 45))

    # noyes
    ghd.create_gym_hour(noyes.id, 0, dt.time(11, 30), dt.time(23, 30))
    for n in range(1, 6):
      ghd.create_gym_hour(noyes.id, n, dt.time(7), dt.time(23, 30))
    ghd.create_gym_hour(noyes.id, 6, dt.time(11, 30), dt.time(22))

    # appel
    ghd.create_gym_hour(appel.id, 0, dt.time(9), dt.time(13))
    for n in range(1, 6):
      ghd.create_gym_hour(appel.id, n, dt.time(15), dt.time(23, 30))
    ghd.create_gym_hour(appel.id, 6, dt.time(9), dt.time(13))

    # adding populartimes to db
    print 'Adding popular_times to db...'
    # helen_newman
    kwargs = {}
    kwargs["monday"] = "[15,25,27,22,21,31,47,53,45,34,36,52,70,75,60,35,14,0]"
    kwargs["tuesday"] = "[16,26,36,45,50,50,46,40,38,42,52,59,59,56,51,36,15]"
    kwargs["wednesday"] = \
        "[17,23,23,17,14,23,40,50,45,35,33,42,52,55,47,33,17,5]"
    kwargs["thursday"] = \
        "[12,20,28,34,37,37,37,39,47,57,67,70,62,47,34,32,26,5]"
    kwargs["friday"] = "[19,25,21,17,19,26,34,38,38,40,46,56,64,64,54,37,20,6]"
    kwargs["saturday"] = "[26,44,42,30,29,35,42,43,38,28,17,8]"
    kwargs["sunday"] = "[19,31,32,23,26,43,59,57,51,51,47,34,17,3]"
    kwargs["gym_id"] = helen_newman.id
    ptl = Ptl(**kwargs)
    db_utils.commit_model(ptl)

    # teagle_up
    kwargs = {}
    kwargs["monday"] = "[14,27,41,53,60,58,50,44,45,56,69,74,64,43,22,8]"
    kwargs["tuesday"] = "[16,26,35,43,53,63,67,61,53,50,52,51,44,30,16,6]"
    kwargs["wednesday"] = "[21,46,38,40,58,62,48,34,35,51,68,75,65,47,26,11]"
    kwargs["thursday"] = "[16,26,37,46,52,53,52,51,53,53,47,45,58,59,32,7]"
    kwargs["friday"] = "[12,26,32,38,48,56,54,50,52,53,44,26,11]"
    kwargs["saturday"] = "[9,17,27,36,41,36,24]"
    kwargs["sunday"] = "[3,13,21,24,34,36,14]"
    kwargs["gym_id"] = teagle_up.id
    ptl = Ptl(**kwargs)
    db_utils.commit_model(ptl)

    # teagle_down
    kwargs = {}
    kwargs["monday"] = "[14,27,41,53,60,58,50,44,45,56,69,74,64,43,22,8]"
    kwargs["tuesday"] = "[16,26,35,43,53,63,67,61,53,50,52,51,44,30,16,6]"
    kwargs["wednesday"] = "[21,46,38,40,58,62,48,34,35,51,68,75,65,47,26,11]"
    kwargs["thursday"] = "[16,26,37,46,52,53,52,51,53,53,47,45,58,59,32,7]"
    kwargs["friday"] = "[12,26,32,38,48,56,54,50,52,53,44,26,11]"
    kwargs["saturday"] = "[9,17,27,36,41,36,24]"
    kwargs["sunday"] = "[3,13,21,24,34,36,14]"
    kwargs["gym_id"] = teagle_down.id
    ptl = Ptl(**kwargs)
    db_utils.commit_model(ptl)

    # noyes
    kwargs = {}
    kwargs["monday"] = "[4,11,20,26,26,24,24,29,39,48,51,48,47,52,52,38,17]"
    kwargs["tuesday"] = "[8,13,17,17,17,20,27,36,45,50,51,51,56,64,67,55,33]"
    kwargs["wednesday"] = "[5,11,18,23,23,20,20,26,38,48,56,63,71,70,56,34,14]"
    kwargs["thursday"] = "[9,16,21,21,17,13,16,26,41,53,54,51,55,67,69,51,24]"
    kwargs["friday"] = "[2,7,14,17,17,15,19,32,50,58,56,51,52,52,45,30,15]"
    kwargs["saturday"] = "[25,36,46,56,58,50,47,53,58,50,35]"
    kwargs["sunday"] = "[18,36,44,39,33,38,45,52,63,75,70,45,18]"
    kwargs["gym_id"] = noyes.id
    ptl = Ptl(**kwargs)
    db_utils.commit_model(ptl)

    # appel
    kwargs = {}
    kwargs["monday"] = "[15,25,27,22,21,31,47,53,45,34,36,52,70,75,60,35,14,0]"
    kwargs["tuesday"] = "[16,26,36,45,50,50,46,40,38,42,52,59,59,56,51,36,15]"
    kwargs["wednesday"] = \
        "[17,23,23,17,14,23,40,50,45,35,33,42,52,55,47,33,17,5]"
    kwargs["thursday"] = \
        "[12,20,28,34,37,37,37,39,47,57,67,70,62,47,34,32,26,5]"
    kwargs["friday"] = "[19,25,21,17,19,26,34,38,38,40,46,56,64,64,54,37,20,6]"
    kwargs["saturday"] = "[26,44,42,30,29,35,42,43,38,28,17,8]"
    kwargs["sunday"] = "[19,31,32,23,26,43,59,57,51,51,47,34,17,3]"
    kwargs["gym_id"] = appel.id
    ptl = Ptl(**kwargs)
    db_utils.commit_model(ptl)

    prefix = "https://raw.githubusercontent.com/cuappdev/assets/mas\
ter/fitness/class_tags/"
    # adding class_tags to db
    print 'Adding class_tags to db...'
    _, barre = ctd.create_class_tag('Barre')
    _, dance = ctd.create_class_tag('Dance')
    _, energy = ctd.create_class_tag('Energy')
    energy.image_url = prefix + "energy.png"
    db_utils.commit_model(energy)
    _, zen = ctd.create_class_tag('Zen')
    zen.image_url = prefix + "zen.png"
    db_utils.commit_model(zen)
    _, strength = ctd.create_class_tag('Strength')
    strength.image_url = prefix + "strength.png"
    db_utils.commit_model(strength)
    _, intensity = ctd.create_class_tag('Intensity')
    intensity.image_url = prefix + "intensity.png"
    db_utils.commit_model(intensity)
    _, cardio = ctd.create_class_tag('Cardio')
    cardio.image_url = prefix + "cardio.png"
    db_utils.commit_model(cardio)
    _, cardio_training = ctd.create_class_tag('Cardio Training')
    _, toning = ctd.create_class_tag('Toning')
    toning.image_url = prefix + "toning.png"
    db_utils.commit_model(toning)
    _, spinning = ctd.create_class_tag('Spinning')
    _, yoga = ctd.create_class_tag('Yoga')
    _, hiit = ctd.create_class_tag('H.I.I.T')
    _, strength_training = ctd.create_class_tag('Strength Training')
    _, taichi = ctd.create_class_tag('T\'ai Chi')

    # parse csv
    tags = open('tags-grid-view.csv', 'r')
    tags.readline()
    line = tags.readline()
    while line != '':
        first = str.find(line, ',')
        class_name = line[:first]
        class_desc = cdd.get_class_desc_by_name(class_name)
        # if class_desc is not in db
        if class_desc == None:
            line = tags.readline()
            continue
        # tags
        second = str.find(line, "\",")
        class_tags = line[first+2:second]
        for tag_name in str.split(class_tags, ','):
            tag = ctd.get_class_tag_by_name(tag_name)
            tag.class_descs.append(class_desc)
            db_utils.commit_model(tag)
        # categories
        third = str.find(line, '\"', second+1)
        if third == -1:
            fourth = str.find(line, ',', second+2)
            category_names = [line[second+2:fourth]]
        else:
            fourth = str.find(line, '\",', third)
            categories = line[third+1:fourth]
            category_names = str.split(categories, ',')
        for category_name in category_names:
            category = ctd.get_class_tag_by_name(category_name)
            category.class_descs.append(class_desc)
            db_utils.commit_model(category)
        # loop
        line = tags.readline()

    # adding gym_locations
    print 'Adding gym_locations to db...'
    # appel_fitness_center
    appel_fitness_center = gd.get_gym_by_name("Appel Commons - Fitness Center")
    appel_fitness_center.location_gym_id = appel.id
    db_utils.commit_model(appel_fitness_center)
    # noyes_mulipurpose
    noyes_mulipurpose = gd.get_gym_by_name("Noyes Multipurpose Room")
    noyes_mulipurpose.location_gym_id = noyes.id
    db_utils.commit_model(noyes_mulipurpose)
    # hn_dance_studio
    hn_dance_studio = gd.get_gym_by_name("Helen Newman Hall Dance Studio")
    hn_dance_studio.location_gym_id = helen_newman.id
    db_utils.commit_model(hn_dance_studio)
    # teagle_multipurpose
    teagle_multipurpose = gd.get_gym_by_name("Teagle Multipurpose Room")
    teagle_multipurpose.location_gym_id = teagle_up.id
    db_utils.commit_model(teagle_multipurpose)
    # teagle_pool
    teagle_pool = gd.get_gym_by_name("Teagle Small Pool")
    teagle_pool.location_gym_id = teagle_down.id
    db_utils.commit_model(teagle_pool)
    # bartels_ramin
    bartels_ramin = gd.get_gym_by_name("Bartels Hall - Ramin Room")
    bartels_ramin.location_gym_id = bartel.id
    db_utils.commit_model(bartels_ramin)
    # appel_multipurpose
    appel_multipurpose = gd.get_gym_by_name("Appel Commons - Multipurpose Room")
    appel_multipurpose.location_gym_id = appel.id
    db_utils.commit_model(appel_multipurpose)
    # hn_classroom
    hn_classroom = gd.get_gym_by_name("Helen Newman Hall Classroom")
    hn_classroom.location_gym_id = helen_newman.id
    db_utils.commit_model(hn_classroom)
    # hn_pool
    hn_pool = gd.get_gym_by_name("Helen Newman Hall Pool")
    hn_pool.location_gym_id = helen_newman.id
    db_utils.commit_model(hn_pool)

if __name__ == '__main__':
  delete_migrations()
  setup_dbs()
  init_data()
