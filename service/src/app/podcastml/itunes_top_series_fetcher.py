import json
import urllib
from multiprocessing.dummy import Pool as ThreadPool

# Static iTunes URL that has a json of all podcast genres (id=26 corresponds to podcasts)
genre_lookup_url = 'https://itunes.apple.com/WebObjects/MZStoreServices.woa/ws/genres?id=26'

# URL to find top podcast episodes for a given genre
general_url = 'https://itunes.apple.com/us/rss/toppodcasts{}/json'

def read_url(url):
  response = urllib.urlopen(url)
  return json.loads(response.read())

def fetch_genres():
  tuples = [] # will have entries of type (id:int, name:string)
  data = read_url(genre_lookup_url)
  genres = data['26']['subgenres']
  for genre in genres.values():
    tuples.append((int(genre['id']), str(genre['name'])))
    if 'subgenres' in genre:
      for subgenre in genre['subgenres'].values():
        tuples.append((int(subgenre['id']), str(subgenre['name'])))
  return tuples

def fetch_top_series(genre=None):
  url = general_url.format('') if genre is None \
    else general_url.format('/genre={}'.format(genre))
  data = read_url(url)
  series_ids = [int(entry['id']['attributes']['im:id'])
                for entry in data['feed']['entry']]
  return genre, series_ids

def fetch_series_all_genres(num_threads=10):
  genre_tuples = fetch_genres()
  genre_ids = [gid for (gid, _) in genre_tuples]
  genre_ids.append(None)
  pool = ThreadPool(num_threads)
  results = pool.map(fetch_top_series, genre_ids)
  pool.close()
  pool.join()
  return results
