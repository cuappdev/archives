from . import *
import datetime

def create_event(event_type_id, payload, timestamp):
  event_type = event_types_dao.get_event_type_by_id(event_type_id)

  if event_type is None:
    raise Exception('Event type does not exist.')

  event_types_dao.verify_fields(event_type_id, payload)
  event = Event(event_type_id=event_type_id,
                payload=payload,
                timestamp=timestamp)
  try:
    db_utils.commit_model(event)
    return True, event
  except Exception as e: # pylint: disable=W0703
    return False, e

def create_events(app_id, events):
  succeeded = []
  failed = []

  event_type_names = {event['event_type'] for event in events \
                      if 'event_type' in event}

  event_types = {event_type.name: event_type for event_type in \
                 event_types_dao.get_event_types_by_names(app_id,
                                                          event_type_names)}
  new_event_types = {}
  events_to_add = []

  for event in events:
    try:
      name = event['event_type']
      payload = event['payload']

      if name not in event_types and name not in new_event_types:
        new_event_types[name] = {
            'name': name,
            'fields_info': event_types_dao.generate_fields_info(payload)
        }

      events_to_add.append(event)
    except Exception as e: #pylint:disable=broad-except
      failed.append({'message': str(e), 'event': event})

  for event_type in \
      event_types_dao.create_event_types(app_id, new_event_types.values())[0]:
    event_types[event_type.name] = event_type

  for event in events_to_add:
    try:
      try:
        event_type = event_types[event['event_type']]
      except KeyError:
        raise Exception('Invalid event type.')

      try:
        payload = event['payload']
      except KeyError:
        raise Exception('Invalid payload.')

      try:
        try:
          timestamp = datetime.datetime.strptime(event['timestamp'],
                                                 '%Y-%m-%d %H:%M:%S.%f %Z')
        except ValueError:
          timestamp = datetime.datetime.strptime(event['timestamp'],
                                                 '%Y-%m-%d %H:%M:%S %Z')
      except Exception: #pylint:disable=broad-except
        raise Exception('Invalid timestamp.')

      event_types_dao.verify_fields(event_type.id, payload)
      newEvent = Event(event_type_id=event_type.id, payload=payload,
                       timestamp=timestamp)
      succeeded.append(newEvent)
    except Exception as e: #pylint:disable=broad-except
      failed.append({'message': str(e), 'event': event})

  db_utils.commit_models(succeeded)
  return succeeded, failed

def get_event_by_id(event_id):
  return Event.query.filter(Event.id == event_id).first()
