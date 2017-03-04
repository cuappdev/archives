from abc import ABCMeta, abstractmethod

class Storer(object):
  """Abstract storer class"""

  __metaclass__ = ABCMeta

  def store(self, result_json):
    """
    Given a `result_json` with complete
    series and episode info, store it
    accordingly
    """
    pass # Leave up to implementation 
