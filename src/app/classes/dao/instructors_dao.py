from . import *

def get_instructor_by_id(instructor_id):
  return Instructor.query.filter(Instructor.id == instructor_id).first()

def get_instructor_by_email(email):
  return Instructor.query.filter(Instructor.email == email).first()

def create_instructor(email, first_name='', last_name=''):
  optional_instructor = get_instructor_by_email(email)

  if optional_instructor is not None:
    return False, optional_instructor

  if first_name == '' and last_name == '':
    raise Exception('Both first_name and last_name are not initialized')

  instructor = Instructor(
      first_name=first_name,
      last_name=last_name,
      email=email
  )
  db_utils.commit_model(instructor)
  return True, instructor
