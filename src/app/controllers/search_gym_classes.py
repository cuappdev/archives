from . import *
from flask import abort
import _strptime

class SearchGymClassesController(AppDevController):
  def get_path(self):
    return '/search_gymclass_instances/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    date = None
    if "date" in request.args:
      date = datetime.datetime.strptime(request.args["date"],'%m/%d/%Y')
    else:
      date = datetime.datetime.today()

    required_args = ['start_time', 'end_time']
    req_arg_values = {}
    for arg in required_args:
      if arg not in request.args:
        abort(
          400,
          'Required parameter missing. Required params are ' + ', '.join(
            [str(x) for x in required_args]
          )
        )
      req_arg_values[arg] = datetime.datetime.strptime(
        request.args[arg], '%I:%M%p'
      ).replace(
        year=date.year,
        month=date.month,
        day=date.day
      )

    optional_args = ['gym_ids', 'class_desc_ids', 'instructor_ids']
    opt_arg_values = {}
    for arg in optional_args:
      if arg in request.args:
        arg_array = request.args[arg].strip("[]").split(",")
        arg_array = [v for v in arg_array if v.isdigit()]
        if not arg_array:
          abort(
            400,
            'Incorrect parameter value. Params must have ids: ' + ', '.join(
              [str(x) for x in optional_args]
              )
            )
        opt_arg_values[arg] = arg_array
      else:
        opt_arg_values[arg] = None

    all_gymclasses = gymclass_dao.get_all_classes()

    if opt_arg_values["class_desc_ids"]:
      gym_classes = []
      all_class_descs = class_tags_dao.get_class_descs_by_tag(
        opt_arg_values["class_desc_ids"]
      )
      for class_desc in all_class_descs:
        some_gym_classes = gymclass_dao.get_gym_classes_by_class_desc_id(
          class_desc.id
        )
        gym_classes.extend(some_gym_classes)
      all_gymclasses = gym_classes

    if opt_arg_values["instructor_ids"]:
      all_gymclasses = \
        [c for c in all_gymclasses
          if str(c.instructor_id) in opt_arg_values["instructor_ids"]]

    all_gymclass_instances = []
    for gym_class in all_gymclasses:
      some_gymclass_instances = \
        gymclassinstance_dao.get_gym_class_instances_by_gym_class(
        gym_class.id, None)
      all_gymclass_instances.extend(some_gymclass_instances)

    gymclass_instances = []
    for gymclass_instance in all_gymclass_instances:
      if (
      not (opt_arg_values["gym_ids"] and str(gymclass_instance.gym_id) not in \
        opt_arg_values["gym_ids"]) and
      not (gymclass_instance.is_cancelled) and
      not (gymclass_instance.start_dt < req_arg_values["start_time"] ) and
      not (gymclass_instance.start_dt + gymclass_instance.duration > \
        req_arg_values["end_time"] ) ):
        gymclass_instances.append(gymclass_instance)

    serialized_gymclass_instances = []
    for gymclass_instance in gymclass_instances:
      gci = gymclassinstance_dao.serialize_gym_class_instance(
        gymclass_instance
      )
      serialized_gymclass_instances.append(gci)

    return serialized_gymclass_instances
