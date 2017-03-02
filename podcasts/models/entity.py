import json 

class Entity(object):
  """Parent of all models of this driver"""

  def to_json(self):
    """JSON representation of the episode"""
    return json.dumps(self.__dict__)

  def _build_date_str(self, d):
    """Private - builds a date, given `d`"""
    if d is not None: return str(d.tm_mon) + '-' + str(d.tm_mday) + '-' + str(d.tm_year)
    else: return ''
