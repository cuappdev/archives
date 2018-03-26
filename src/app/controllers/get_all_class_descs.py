from . import *
import datetime

class GetAllClassDescsController(AppDevController):

  def get_path(self):
    return '/class_descs/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    class_descs = class_descs_dao.get_all_class_descs()
    serialized_classes = [class_desc_schema.dump(cd).data for cd in class_descs]

    return serialized_classes
