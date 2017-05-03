==========
py-podcast
==========

iTunes podcast data retrieval and storage utilizing `iTunes Search API`_ and `iTunes Podcast Preview`_

.. _`iTunes Search API`: https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/
.. _`iTunes Podcast Preview`: https://itunes.apple.com/us/genre/podcasts/id26?mt=2

Installation
------------

To install ``py-podcast`` ::

  pip install py-podcast

Usage
-----

Below indicates ways you can use the various drivers and workers of this package ::

  # General imports
  import sys
  import logging

  # Drivers and crawlers
  import podcasts
  from podcasts.series_driver import SeriesDriver
  from podcasts.episodes_driver import EpisodesDriver
  from podcasts.site_crawler import SiteCrawler

  # Storers
  from podcasts.storers.json_storer import JsonStorer

  # Constants
  DIRECTORY = 'csv'
  JSON_DIR  = 'jsons'

  logging.getLogger('py-podcast').disabled = False # Change to `True` if you don't want logging

  # Series
  genre_urls = ['https://itunes.apple.com/us/genre/podcasts-business/id1321?mt=2']
  SeriesDriver(DIRECTORY).get_series_from_urls(genre_urls)

  # Episodes
  EpisodesDriver(DIRECTORY, JsonStorer(JSON_DIR)).eps_from_series()


Tests
-----

These have yet to be written, but this package has been hand-tested thoroughly.
