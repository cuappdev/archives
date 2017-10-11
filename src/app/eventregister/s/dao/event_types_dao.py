from . import *

TYPES = ['str', 'int', 'float']

def create_event_type(app_id, name, creator, fields_info):
  event_type = get_event_type_by_name(app_id, name)

  if event_type is not None:
    return False, event_type

  verify_fields_info(fields_info)

  app = applications_dao.get_app_by_id(app_id)

  if app is None:
    raise Exception('App does not exist.')

  event_type = EventType(
      name=name,
      creator=creator,
      application_id=app_id,
      fields_info=fields_info
  )
  db_utils.commit_model(event_type)
  return True, event_type

def get_event_type_by_name(app_id, name):
  return EventType.query.filter(EventType.application_id == app_id,
                                EventType.name == name).first()

def get_event_type_by_id(event_type_id):
  return EventType.query.filter(EventType.id == event_type_id).first()

def verify_fields_info(fields_info): #TODO: change logic later
  for field in fields_info:
    metadata = fields_info[field]
    if 'type' not in metadata:
      raise Exception('Type missing for field %s' % field)
    elif metadata['type'] not in TYPES:
      raise Exception('Type invalid for field %s' % field)
    elif 'required' not in metadata:
      raise Exception('Required status missing for field %s' % field)
    elif not isinstance(metadata['required'], bool):
      raise Exception('Required status invalid for field %s' % field)
    elif not metadata['required']:
      if 'default' not in metadata:
        raise Exception('Default value missing for field %s' % field)
      elif not isinstance(metadata['default'], metadata['type']):
        raise Exception('Default value invalid for field %s' % field)

  return True

def verify_fields(event_type_id, payload): #TODO: change logic later
  event_type = get_event_type_by_id(event_type_id)

  if event_type is None:
    raise Exception('Event type does not exist.')

  fields_info = event_type.fields_info

  for field in fields_info:
    metadata = fields_info[field]

    if field not in payload:
      if metadata['required']:
        raise Exception('Missing required field %s in payload' % field)
      else:
        payload[field] = metadata['default']
    elif field in payload and type(payload[field]).__name__ != metadata['type']:
      raise Exception('Invalid type for field %s in payload' % field)

  return True

def get_events(event_type_id):
  event_type = get_event_type_by_id(event_type_id)

  if event_type is None:
    raise Exception('Event type does not exist.')

  return [event.id for event in event_type.events]
