from . import *

class ToggleFavoriteController(AppDevController):

  def get_path(self):
    return '/favorite/<device_id>/<gymclass_id>/'

  def get_methods(self):
    return ['POST', 'GET']

  def content(self, **kwargs):
    device_id = request.view_args['device_id']
    gymclass_id = request.view_args['gymclass_id']
    user = users_dao.get_user_by_device_id(device_id)
    user_classes = users_dao.get_user_classes(user.id)
    gymclass = gymclass_dao.get_gym_class_by_id(gymclass_id)
    # check if gymclass is already favorited
    if gymclass in user_classes:
        user_classes.remove(gymclass)
    else:
        user_classes.append(gymclass)
    user.gym_classes = user_classes
    db_utils.db_session_commit()
    return user_schema.dump(user).data
