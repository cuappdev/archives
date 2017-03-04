import json
from datetime import datetime

# https://goo.gl/jPXD44
def json_serial(obj):
  """JSON serializer for objects not serializable by default json code"""

  if isinstance(obj, datetime):
    serial = obj.isoformat()
    return serial
  raise TypeError ("Type not serializable")


class Entity(object):
  """Parent of all models of this driver"""

  def to_json(self):
    """JSON representation of the episode"""
    return json.dumps(self.__dict__, default=json_serial)

  def _build_date_str(self, d):
    """Private - builds a date, given `d`"""
    if d is not None:
      return datetime(d.tm_year, d.tm_mon, d.tm_mday, d.tm_hour, d.tm_min, d.tm_sec)
    else:
      return None
