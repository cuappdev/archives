import _strptime
import json
from flask import abort
from . import *

class SearchGymClassesController(AppDevController):
  def get_path(self):
    return '/search_gymclass_instances/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    """Search route for gym classes.

    required arguments:
    "<start_time>" -- the starting time, string formatted HH:MMPM
    "<end_time>" -- the ending time, string formatted HH:MMPM

    optional arguments:
    "<instructor_ids>" -- array of instructor_ids
    "<gym_ids>" -- array of gym ids
    "<class_desc_ids>" -- array of class_desc ids
    "<date>" -- date is string formatted MM/DD/YYYY

    """
    date = datetime.datetime.today()
    if "date" in request.args:
      date = datetime.datetime.strptime(request.args["date"], '%m/%d/%Y')

    # get required arguments
    required_args = {'start_time': None, 'end_time': None}
    for key in required_args:
      if key not in request.args:
        abort(400, 'Required parameter missing. Required params are ' +
              ', '.join(required_args))
      required_args[key] = datetime.datetime.strptime(
        request.args[key], '%I:%M%p'
      ).replace(year=date.year, month=date.month, day=date.day)

    # get optional arguments
    optional_args = {'gym_ids': None, 'class_desc_ids': None,
                     'instructor_ids': None}
    for key in optional_args:
      if key in request.args:
        arg_array = json.loads(request.args[key])
        arg_array = [v for v in arg_array if isinstance(v, int)]
        if not arg_array:
          abort(400, 'Incorrect parameter value. Params must have ids: ' +
                ', '.join(optional_args))
        optional_args[key] = arg_array

    # filter based on arguments
    all_gymclasses = gymclass_dao.get_all_classes()

    if optional_args["class_desc_ids"]:
      gym_classes = []
      all_class_descs = class_descs_dao.get_class_descs_by_ids(
          optional_args["class_desc_ids"]
      )
      for class_desc in all_class_descs:
        some_gym_classes = gymclass_dao.get_gym_classes_by_class_desc_id(
            class_desc.id
        )
        gym_classes.extend(some_gym_classes)
      all_gymclasses = gym_classes

    if optional_args['instructor_ids']:
      gymclasses = []
      for c in all_gymclasses:
        if c.instructor_id in optional_args["instructor_ids"]:
          gymclasses.append(c)
      all_gymclasses = gymclasses

    all_gci = []
    for gym_class in all_gymclasses:
      some_gymclass_instances = \
        gymclassinstance_dao.get_gym_class_instances_by_gym_class(
          gym_class.id, None)
      all_gci.extend(some_gymclass_instances)

    if optional_args['gym_ids']:
      gc = []
      for c in all_gci:
        if c.gym_id in optional_args["gym_ids"]:
          gc.append(c)
      all_gci = gc

    gymclass_instances = []
    for c in all_gci:
      if not c.is_cancelled and c.start_dt >= required_args["start_time"] \
        and c.start_dt + c.duration <= required_args["end_time"]:
        gymclass_instances.append(c)

    serialized_gymclass_instances = []
    for gymclass_instance in gymclass_instances:
      gci = \
        gymclassinstance_dao.serialize_gym_class_instance(gymclass_instance)
      serialized_gymclass_instances.append(gci)

    return serialized_gymclass_instances
