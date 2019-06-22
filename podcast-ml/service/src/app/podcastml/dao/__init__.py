from app.podcastml.models._all import *
from app.podcastml.utils import db_utils

def format_list(object_list):
  return ','.join(map(str, object_list))

def extract_list(object_list_string):
  return [int(element) for element in object_list_string.split(',')]

def get_list(model, id_field, id_query, list_field):
  optional_model = model.query \
    .filter(getattr(model, id_field) == id_query).first()
  if optional_model:
    return extract_list(getattr(optional_model, list_field))
  else:
    raise Exception('No {} where {}={} exists.'
                    .format(model, id_field, id_query))
