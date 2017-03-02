import json

class Episode(object):

  def __init__(self, series_id, series_title, series_image_url, entry):
    """Constructor"""

    # Fill fields
    self.series_id    = series_id
    self.series_title = series_title
    self.image_url    = series_image_url
    self.title        = '' if 'title' not in entry else entry['title']
    self.author       = '' if 'author' not in entry else entry['author']
    self.summary      = '' if 'summary_detail' not in entry else entry['summary_detail']['value']
    self.pub_date     = '' if 'published_parsed' not in entry else self._build_date_str(entry['published_parsed'])
    self.duration     = '' if 'itunes_duration' not in entry else entry['itunes_duration']
    self.tags         = [] if 'tags' not in entry else [t['term'] for t in entry['tags']]

    # Grab audio_url
    self.audio_url = None
    for l in entry['links']:
      if ('type' in l) and ('audio' in l['type']): self.audio_url = l['href']; break

  def to_json(self):
    """JSON representation of the episode"""
    return json.dumps(self.__dict__)

  def _build_date_str(self, d):
    """Private - builds a date, given `d`"""
    if d is not None: return str(d.tm_mon) + '-' + str(d.tm_mday) + '-' + str(d.tm_year)
    else: return ''
