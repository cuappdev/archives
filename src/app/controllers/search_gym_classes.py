from . import *
from flask import abort
import _strptime

class SearchGymClassesController(AppDevController):
  def get_path(self):
    return '/search_gymclass_instances/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):

    start_time = request.args.get('start_time')
    if start_time is None:
      abort(400, "Need a start time")

    end_time = request.args.get('end_time')
    if end_time is None:
     abort(400, "Need an end time")

    fitness_centers = request.args.getlist("fitness_centers")
    for fitness_center in fitness_centers:
      if not fitness_center.isdigit():
        abort(400, "Fitness centers must be id values")

    classtypes = request.args.getlist("classtypes")
    for classtype in classtypes:
      if not classtype.isdigit():
        abort(400, "Classtypes must be id values")

    instructors = request.args.getlist("instructors")
    for instructor in instructors:
      if not instructor.isdigit():
        abort(400, "Instructors must be id values")

    start_datetime = datetime.datetime.strptime(start_time, '%I:%M%p') \
      .replace(year=datetime.datetime.today().year,
        month=datetime.datetime.today().month,
        day=datetime.datetime.today().day)

    end_datetime = datetime.datetime.strptime(end_time, '%I:%M%p') \
      .replace(year=datetime.datetime.today().year,
        month=datetime.datetime.today().month,
        day=datetime.datetime.today().day)

    all_gymclasses = gymclass_dao.get_all_classes()

    if classtypes:
      gym_classes = []
      all_class_descs = class_tags_dao.get_class_descs_by_tag(classtypes)
      for class_desc in all_class_descs:
        some_gym_classes = \
          gymclass_dao.get_gym_classes_by_class_desc_id(class_desc.id)
        gym_classes.extend(some_gym_classes)
      all_gymclasses = gym_classes

    if instructors:
      gym_classes = []
      for gym_class in all_gymclasses:
        # need to convert to string
        if str(gym_class.instructor_id) in instructors:
          gym_classes.append(gym_class)
      all_gymclasses = gym_classes

    all_gymclass_instances = []

    for gym_class in all_gymclasses:
      some_gymclass_instances= \
        gymclassinstance_dao.get_gym_class_instances_by_gym_class(
        gym_class.id, None)
      all_gymclass_instances.extend(some_gymclass_instances)

    gymclass_instances = []

    for gymclass_instance in all_gymclass_instances:
      if fitness_centers:
        # need to convert to string
        if str(gymclass_instance.gym_id) not in fitness_centers:
          continue
      if gymclass_instance.is_cancelled:
        continue
      if gymclass_instance.start_dt < start_datetime:
        continue
      if gymclass_instance.start_dt+gymclass_instance.duration > end_datetime:
        continue
      gymclass_instances.append(gymclass_instance)

    serialized_gymclass_instances = []

    for gymclass_instance in gymclass_instances:
      gci = gymclassinstance_dao.serialize_gym_class_instance(
       gymclass_instance
      )
      serialized_gymclass_instances.append(gci)

    return serialized_gymclass_instances
