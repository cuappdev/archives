from flask import request, render_template, jsonify, redirect
from appdev.controllers import *
from app.dao import class_descs_dao, \
    class_tags_dao, \
    gyms_dao, \
    gymclass_dao, \
    gymclassinstance_dao, \
    gymhours_dao, \
    instructors_dao, \
    populartimeslist_dao, \
    users_dao

from app.models._all import *

# Serializers
gym_schema = GymSchema()
gymclass_schema = GymClassSchema()
instructor_schema = InstructorSchema()
class_desc_schema = ClassDescSchema()
gym_hour_schema = GymHourSchema()
user_schema = UserSchema()
populartimeslist_schema = PopularTimesListSchema()
