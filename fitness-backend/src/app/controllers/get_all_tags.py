from . import *

class GetAllTagsController(AppDevController):

  def get_path(self):
    return '/tags'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    all_tags = class_tags_dao.get_all_tags()
    return [class_tag_schema.dump(t).data for t in all_tags]
