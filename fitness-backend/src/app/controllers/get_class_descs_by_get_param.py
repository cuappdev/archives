from flask import abort
from . import *

class GetClassDescsByGetParamController(AppDevController):

  def get_path(self):
    return '/class_descs/<id>'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    _id = request.view_args.get('id')
    _type = request.args.get('type')

    if _type is None or (_type != "tag_id" and _type != "id"):
      abort(400, 'Param "type" missing or incorrect.')

    if _type == "id":
      class_desc = class_descs_dao.get_class_desc_by_id(_id)
      serialized_class_desc = class_desc_schema.dump(class_desc).data
      return serialized_class_desc

    # tag_id
    class_tag = class_tags_dao.get_class_tag_by_id(_id)
    class_descs = class_tags_dao.get_class_descs_by_tag([class_tag.id])
    serialized_classes = \
        [class_desc_schema.dump(cd).data for cd in class_descs]
    return serialized_classes
