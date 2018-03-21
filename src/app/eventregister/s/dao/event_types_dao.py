from . import *

TYPES = {'str': str, 'int': int, 'float': float, 'bool': bool}

def create_event_type(app_id, name, fields_info):
  app = applications_dao.get_app_by_id(app_id)

  if app is None:
    raise Exception('App does not exist.')

  event_type = get_event_type_by_name(app_id, name)

  if event_type is not None:
    return False, event_type

  verify_fields_info(fields_info)

  event_type = EventType(
      name=name,
      application_id=app_id,
      fields_info=fields_info
  )
  db_utils.commit_model(event_type)
  return True, event_type

def create_event_types(app_id, event_types):
  if applications_dao.get_app_by_id(app_id) is None:
    raise Exception('App does not exist.')

  succeeded = []
  failed = []

  for event_type in event_types:
    try:
      try:
        name = event_type['name']
      except KeyError:
        raise Exception('Invalid event type name.')

      try:
        fields_info = event_type['fields_info']
      except KeyError:
        raise Exception('Invalid event type field specification.')

      if get_event_type_by_name(app_id, name) is not None:
        raise Exception('Event type already exists.')

      verify_fields_info(fields_info)

      event_type = EventType(
          name=name,
          application_id=app_id,
          fields_info=fields_info
      )

      succeeded.append(event_type)
    except Exception as e: #pylint:disable=broad-except
      failed.append({'message': str(e), 'event_type': event_type})

  db_utils.commit_models(succeeded)
  return succeeded, failed

def generate_fields_info(payload):
  fields_info = {}

  for field in payload:
    field_info = {'required': True}
    data = payload[field]

    for type_name in TYPES:
      if isinstance(data, TYPES[type_name]):
        field_info['type'] = type_name
        break

    if 'type' not in field_info:
      raise Exception('Unable to infer type from value.')

    fields_info[field] = field_info

  return fields_info

def get_event_type_by_name(app_id, name):
  return EventType.query.filter(EventType.application_id == app_id,
                                EventType.name == name).first()

def get_event_types_by_names(app_id, names):
  return EventType.query.filter(EventType.application_id == app_id,
                                EventType.name.in_(names)).all()

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
      elif not isinstance(metadata['default'], TYPES[metadata['type']]):
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
    elif field in payload \
         and not isinstance(payload[field], TYPES[metadata['type']]):
      raise Exception('Invalid type for field %s in payload' % field)

  return True

def get_events(event_type_id):
  event_type = get_event_type_by_id(event_type_id)

  if event_type is None:
    raise Exception('Event type does not exist.')

  return event_type.events
