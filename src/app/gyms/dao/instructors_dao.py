from . import *

def get_all_instructors():
  return Instructor.query.all()

def get_instructor_by_id(instructor_id):
  return Instructor.query.filter(Instructor.id == instructor_id).first()

def get_instructor_by_name(name):
  return Instructor.query.filter(Instructor.name == name).first()

def create_instructor(name):
  optional_instructor = get_instructor_by_name(name)

  if optional_instructor is not None:
    return False, optional_instructor

  instructor = Instructor(name=name)
  db_utils.commit_model(instructor)
  return True, instructor
