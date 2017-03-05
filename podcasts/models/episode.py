import json
from entity import Entity

class Episode(Entity):

  def __init__(self, series, entry):
    """Constructor"""

    # Fill fields
    self.type         = 'episode'
    self.series_id    = series.id
    self.series_title = series.title
    self.image_url_sm = series.image_url_sm
    self.image_url_lg = series.image_url_lg
    self.title        = '' if 'title' not in entry else entry['title']
    self.author       = '' if 'author' not in entry else entry['author']
    self.summary      = '' if 'summary_detail' not in entry else entry['summary_detail']['value']
    self.pub_date     = '' if 'published_parsed' not in entry else self._build_date_str(entry['published_parsed'])
    self.duration     = '' if 'itunes_duration' not in entry else entry['itunes_duration']
    self.tags         = [] if 'tags' not in entry else [t['term'] for t in entry['tags']]

    # Grab audio_url
    self.audio_url = None
    if 'links' in entry:
      for l in entry['links']:
        if ('type' in l) and ('audio' in l['type']): self.audio_url = l['href']; break
