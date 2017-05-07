import json
from entity import Entity

class Episode(Entity):

  def __init__(self, series, title,author,summary,pubDate,duration,tags,audioUrl):
    """Constructor"""

    # Fill fields
    self.type         = 'episode'
    self.seriesId     = series.id
    self.seriesTitle  = series.title # Already encoded
    self.imageUrlSm   = series.imageUrlSm # Already encoded
    self.imageUrlLg   = series.imageUrlLg # Already encoded
    self.title        = title.encode('ascii','ignore')
    self.author       = author.encode('ascii','ignore')
    self.summary      = summary.encode('ascii','ignore')
    self.pubDate      = pubDate
    self.duration     = duration.encode('ascii','ignore')  
    self.tags         = tags

    # Grab audio_url
    self.audioUrl = audioUrl
