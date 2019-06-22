from . import *

class SearchSeriesController(AppDevController):

  def get_path(self):
    return '/search/series/<query>/'

  def get_methods(self):
    return ['GET']

  @authorize
  def content(self, **kwargs):
    user_id = kwargs.get('user').id
    search_name = request.view_args['query']
    offset = request.args['offset']
    max_search = request.args['max']

    possible_series = series_dao.\
        search_series(search_name, offset, max_search, user_id)

    return {'series': [series_schema.dump(s).data for s in possible_series]}
