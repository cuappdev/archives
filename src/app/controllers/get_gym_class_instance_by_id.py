from . import *

class GetGymClassInstanceByIdController(AppDevController):

  def get_path(self):
    return '/gymclassinstance/<id>/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    gymclass_instance_id = request.view_args['id']
    instructor_schema = InstructorSchema()
    class_desc_schema = ClassDescSchema()
    gymclass_instance = gymclassinstance_dao.get_gym_class_instance_by_id(
            gymclass_instance_id
    )
    serialized_gym = {"id": gymclass_instance_id}

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

    return serialized_gym
