#!/usr/bin/python
import sys
import logging
import feedparser
# podfetch imports
from podcasts.series_driver import SeriesDriver
from podcasts.episodes_driver import EpisodesDriver
from podcasts.storers.json_storer import JsonStorer
from podcasts.models.series import Series
import podcasts.itunes as itunes

def grab_from_link():
  # Constants
  DIRECTORY = 'csv'
  JSON_DIR = 'jsons'
  # logging.getLogger('podfetch').disabled = True
  # Series
  genre_urls = \
    ['https://itunes.apple.com/us/genre/podcasts-business/id1321?mt=2']
  SeriesDriver(DIRECTORY).get_series_from_urls(genre_urls)
  # Episodes
  EpisodesDriver(DIRECTORY, JsonStorer(JSON_DIR)).eps_from_series()

def search():
  many_series = itunes.search_podcast_series('Programming')
  return itunes.get_feeds_from_many_series(many_series)

if __name__ == '__main__':
  # grab_from_link()
  print search()
