from . import *

class GetGymClassesByTag(AppDevController):

  def get_path(self):
    return '/gymclass/<tag_name>'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    tag_name = request.view_args['tag_name']
    class_tag = class_tags_dao.get_class_tag_by_name(tag_name)
    gymclasses = class_tags_dao.get_classes_by_tag(class_tag.id)
    return [gymclass_schema.dump(gc).data for gc in gymclasses]
