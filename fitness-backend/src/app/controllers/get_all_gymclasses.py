import json
from . import *

class GymClassesController(AppDevController):

  def get_path(self):
    return '/gymclasses/'

  def get_methods(self):
    return ['GET', 'POST']

  def content(self, **kwargs):
    if request.method == "GET":
      gymclasses = gymclass_dao.get_all_classes()
      serialized_classes = [gymclass_schema.dump(gc).data for gc in gymclasses]
      return serialized_classes

    elif request.method == "POST":
      print(request.form)
      class_ids = json.loads(request.form["class_ids"])
      class_ids = [v for v in class_ids if isinstance(v, int)]
      instances = gymclassinstance_dao.get_gym_class_instances_by_gym_class_ids(
          class_ids)
      serialized_instances = [
          gymclassinstance_schema.dump(i).data
          for i in instances
      ]
      return serialized_instances
