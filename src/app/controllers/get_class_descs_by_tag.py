from . import *

class GetClassDescsByTag(AppDevController):

  def get_path(self):
    return '/class_descs/<tag_id>'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    tag_id = request.view_args['tag_id']
    class_tag = class_tags_dao.get_class_tag_by_id(tag_id)
    class_descs = class_tags_dao.get_class_descs_by_tag([class_tag.id])
    serialized_classes = [class_desc_schema.dump(cd).data for cd in class_descs]
    return serialized_classes
