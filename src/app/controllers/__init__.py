from flask import request, render_template, jsonify, redirect
from appdev.controllers import *
from app.dao import gyms_dao, \
  instructors_dao, \
  gymclass_dao, \
  gymclassinstance_dao, \
  gymhours_dao, \
  users_dao

from app.models._all import *

# Serializers
gym_schema = GymSchema()
instructor_schema = InstructorSchema()
gym_class_instance = GymClassInstanceSchema()
