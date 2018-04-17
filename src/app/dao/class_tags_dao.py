from . import *

def get_class_tag_by_id(class_tag_id):
  return ClassTag.query.filter(ClassTag.id == class_tag_id).first()

def get_class_tag_by_name(name):
  return ClassTag.query.filter(ClassTag.name == name).first()

def get_class_descs_by_tag(tag_id_list):
  result = []
  for tag_id in tag_id_list:
      optional_tag = get_class_tag_by_id(tag_id)
      if optional_tag is None:
        raise Exception('Tag does not exist.')
      result = result + optional_tag.class_descs
  return result

def get_all_tags():
  return ClassTag.query.all()

def create_class_tag(name):
  optional_tag = get_class_tag_by_name(name)

  if optional_tag is not None:
    return False, optional_tag

  # tag does not exist
  class_tag = ClassTag(
      name=name,
  )
  db_utils.commit_model(class_tag)
  return True, class_tag
