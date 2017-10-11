from . import *

def create_event(event_type_id, payload):
  event_type = event_types_dao.get_event_type_by_id(event_type_id)

  if event_type is None:
    raise Exception('Event type does not exist.')

  event_types_dao.verify_fields(event_type_id, payload)
  event = Event(event_type_id=event_type_id, payload=payload)
  try:
    db_utils.commit_model(event)
    return True, event
  except Exception as e:
    return False, e
