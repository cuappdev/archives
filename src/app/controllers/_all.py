from app.controllers.get_all_class_descs import * # pylint: disable=C0413
from app.controllers.get_all_gyms import * # pylint: disable=C0413
from app.controllers.get_all_gymclasses import * # pylint: disable=C0413
from app.controllers.get_all_instructors import * # pylint: disable=C0413
from app.controllers.get_all_tags import * # pylint: disable=C0413
from app.controllers.get_class_desc_by_id import * # pylint: disable=C0413
from app.controllers.get_gym_by_id import * # pylint: disable=C0413
from app.controllers.get_gym_class_instance_by_id import * # pylint: disable=C0413
from app.controllers.get_gym_class_instances import * # pylint: disable=C0413
from app.controllers.get_gym_class_instances_by_date import * # pylint: disable=C0413
from app.controllers.get_class_descs_by_tag import * # pylint: disable=C0413
from app.controllers.get_instructor_by_id import * # pylint: disable=C0413
from app.controllers.toggle_favorite import * # pylint: disable=C0413

controllers = [
    GetAllClassDescsController(),
    GetAllGymsController(),
    GetAllGymClassesController(),
    GetAllTagsController(),
    GetAllInstructorsController(),
    GetClassDescByIdController(),
    GetGymByIdController(),
    GetGymClassInstanceByIdController(),
    GetGymClassInstancesController(),
    GetGymClassInstancesByDate(),
    GetClassDescsByTag(),
    GetInstructorByIdController(),
    ToggleFavoriteController(),
]
