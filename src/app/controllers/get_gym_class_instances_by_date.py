from . import *
import datetime as dt

class GetGymClassInstancesByDate(AppDevController):

  def get_path(self):
    return '/gymclassinstances/date/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    year = request.form['year']
    month = request.form['month']
    day = request.form['day']

    gymclass_instances = \
        gymclassinstance_dao.get_gym_class_instances_by_date(year, month, day)

    serialized_gymclass_instances = []
    for gymclass_instance in gymclass_instances:
        serialized_gym = {"id": gymclass_instance.id}

        # get gymclass
        gym_class = gymclass_dao.get_gym_class_by_id(
                gymclass_instance.gym_class_id
        )

        # get instructor
        instructor = instructors_dao.get_instructor_by_id(
                gymclass.instructor_id
        )
        instructor = instructor_schema.dump(instructor).data
        serialized_gym["instructor"] = instructor

        # get class_desc
        class_desc = class_descs_dao.get_class_desc_by_id(
                gym_class.class_desc_id
        )
        class_desc = class_desc_schema.dump(class_desc).data
        serialized_gym["gym_class"] = gymclass

        serialized_gymclass_instances.append(serialized_gym)

    return serialized_gymclass_instances
