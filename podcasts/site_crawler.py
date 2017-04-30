import requests as r
import constants as c
from lxml import html
import string

# Entity with utilities for iTunes preview site for Podcasts
class SiteCrawler(object):

  def get_genres(self):
    """
    Grab (genre,url) tuples from iTunes Podcast preview
    """
    page = r.get(c.ITUNES_GENRES_URL)
    tree = html.fromstring(page.content)
    elements = tree.xpath("//a[@class='top-level-genre']")
    return [(e.attrib['title']
              .lower()[:(e.attrib['title'].rfind('-')-1)]
              .replace(' ', ''), e.attrib['href'])
              for e in elements]

  def generate_urls_for_genre(self, genre_url):
    """
    Generate URL's for genre
    """
    letters = list(string.ascii_uppercase)
    urls = []
    for letter in letters:
      base = '{}&letter={}'.format(genre_url, letter)
      page = r.get(base)
      tree = html.fromstring(page.content)
      elements = tree.xpath("//ul[@class='list paginate']")
      if len(elements) == 0:
        urls.append(base)
      else:
        for i in xrange(1, len(elements[0].getchildren()) + 1):
          urls.append('{}&page={}#page'.format(base, i))
    return urls

  def all_urls(self):
    """
    All url's to get podcasts
    """
    result = []
    genres = [g[1] for g in self.get_genres()]
    for g_url in genres:
      print 'Getting {}'.format(g_url)
      result.extend(self.generate_urls_for_genre(g_url))
    return result
