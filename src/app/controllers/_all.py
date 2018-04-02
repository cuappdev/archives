from get_all_class_descs import * # pylint: disable=C0413
from get_all_gyms import * # pylint: disable=C0413
from get_all_gymclasses import * # pylint: disable=C0413
from get_all_instructors import * # pylint: disable=C0413
from get_class_desc_by_id import * # pylint: disable=C0413
from get_gym_by_id import * # pylint: disable=C0413
from get_gym_class_instance_by_id import * # pylint: disable=C0413
from get_gym_class_instances import * # pylint: disable=C0413
from get_instructor_by_id import * # pylint: disable=C0413
from toggle_favorite import * # pylint: disable=C0413

controllers = [
    GetAllClassDescsController(),
    GetAllGymsController(),
    GetAllGymClassesController(),
    GetAllInstructorsController(),
    GetClassDescByIdController(),
    GetGymByIdController(),
    GetGymClassInstanceByIdController(),
    GetGymClassInstancesController(),
    GetInstructorByIdController(),
    ToggleFavoriteController(),
]
