from . import *

def create_event(event_type_id, payload):
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

  event_type_names = {event['event_type'] for event in events}
  event_types = {event_type.name: event_type for event_type in \
                 event_types_dao.get_event_types_by_names(event_type_names)}

  for event in events:
    event_type = event_types[event['event_type']]

    try:
      event_types_dao.verify_fields(event_type.id, event['payload'])
      newEvent = Event(event_type_id=event_type.id, payload=event['payload'])
      succeeded.append(newEvent)
    except Exception as e: #pylint:disable=broad-except
      failed.append({'message': e, 'event': event})

  db_utils.commit_models(succeeded)
  return succeeded, failed

def get_event_by_id(event_id):
  return Event.query.filter(Event.id == event_id).first()
