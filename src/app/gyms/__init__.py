from flask import Blueprint
from app import *

gyms = Blueprint('gyms', __name__, url_prefix='/api')

from app.gyms.models._all import * # pylint: disable=C0413

from app.gyms.controllers.get_all_gyms_controller import * # pylint: disable=C0413
from app.gyms.controllers.get_gym_by_id_controller import * # pylint: disable=C0413
from app.gyms.controllers.get_all_instructors_controller import * # pylint: disable=C0413
from app.gyms.controllers.get_instructor_by_id_controller import * # pylint: disable=C0413
from app.gyms.controllers.get_gym_class_instance_by_id_controller import * # pylint: disable=C0413

controllers = [
    GetAllGymsController(),
    GetGymByIdController(),
    GetAllInstructorsController(),
    GetInstructorByIdController(),
    GetGymClassInstanceByIdController(),
]

for controller in controllers:
  gyms.add_url_rule(
      controller.get_path(),
      controller.get_name(),
      controller.response,
      methods=controller.get_methods()
  )
