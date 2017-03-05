#!/usr/bin/python

from series_driver import SeriesDriver
from episodes_driver import EpisodesDriver
from podcasts.site_crawler import SiteCrawler
from podcasts.storers.couchbase_storer import CouchbaseStorer

DIRECTORY  = 'csv'
BUCKET_URL = 'couchbase://localhost:8091/podcasts'

# Grab all series first
# SeriesDriver(DIRECTORY).get_popular(SiteCrawler().get_genres())
# Grab all episodes once we have data stored
EpisodesDriver(DIRECTORY, CouchbaseStorer(BUCKET_URL)).eps_from_series()
