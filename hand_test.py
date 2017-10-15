#!/usr/bin/python

# General imports
import sys
import logging

# Drivers and crawlers
from podcasts.series_driver import SeriesDriver
from podcasts.episodes_driver import EpisodesDriver

# Storers
from podcasts.storers.json_storer import JsonStorer

if __name__ == '__main__':
  # Constants
  DIRECTORY = 'csv'
  JSON_DIR  = 'jsons'
  # logging.getLogger('py-podcast').disabled = True
  # Series
  genre_urls = ['https://itunes.apple.com/us/genre/podcasts-business/id1321?mt=2']
  SeriesDriver(DIRECTORY).get_series_from_urls(genre_urls)
  # Episodes
  EpisodesDriver(DIRECTORY, JsonStorer(JSON_DIR)).eps_from_series()
