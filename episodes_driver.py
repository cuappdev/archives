from podcasts.episode_worker import EpisodeWorker
from os import walk

class EpisodeDriver(object):
  """
  Drives the acquisition of episodes
  based on series that exist in csv's
  stored in `directory`
  """

  def __init__(self, directory):
    """Constructor"""
    self.directory = directory

  def eps_from_series(self):
    """
    Workhorse function that handles grabbing
    series data from csvs and
    """
    # TODO 
    pass
