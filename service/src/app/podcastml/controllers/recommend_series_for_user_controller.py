from . import *

class RecommendSeriesForUserController(AppDevController):

  def get_path(self):
    return '/series/user/<user_id>/'

  def get_methods(self):
    return ['GET']

  @authorize
  def content(self, **kwargs):
    user_id = request.view_args['user_id']
    series_ids = series_for_user_dao.get_series_list_for_user(user_id)
    return {'series_ids': series_ids}
