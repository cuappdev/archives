#!/usr/bin/python

# Drivers and crawlers
from podcasts.series_driver import SeriesDriver
from podcasts.episodes_driver import EpisodesDriver
from podcasts.site_crawler import SiteCrawler

# Storers
from podcasts.storers.json_storer import JsonStorer
from podcasts.storers.couchbase_storer import CouchbaseStorer

# Constants
DIRECTORY  = 'csv'
BUCKET_URL = 'couchbase://localhost:8091/podcasts'
JSON_DIR   = 'data'

# Grab all series first
# SeriesDriver(DIRECTORY).get_popular(SiteCrawler().get_genres()[0:3])
# Grab all episodes once we have data stored
EpisodesDriver(DIRECTORY, JsonStorer(JSON_DIR)).eps_from_series()
