from . import *
import datetime

class GetClassDescByIdController(AppDevController):

  def get_path(self):
    return '/class_desc/<id>/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    class_desc_id = request.view_args['id']
    class_desc = class_descs_dao.get_class_desc_by_id(class_desc_id)
    serialized_class_desc = class_desc_schema.dump(class_desc).data

    return serialized_class_desc
