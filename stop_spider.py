import scrapy
import re

# Spider for parsing stops and their coordinates
class StopSpider(scrapy.Spider):

  # Regex for parsing latitude and longitude  
  lat_lng_regex = r'[-+]?\d*\.\d+|\d+'
  name = "stops"
  start_urls = [
    # URL for the list of all TCAT stops
    'https://tcat.nextinsight.com/allstops.php'
  ]

  # Parse coordinates from the link and return the route and its location
  def parse_coordinates(self, response):
    # Get stop name
    stop = response.css('div.g1-hgroup h1::text').extract_first()
    # Parse coordinates from link in the page
    coordinates = response.css('div.g1-inner li a::attr(href)')[3].extract()
    coordinates = re.findall(StopSpider.lat_lng_regex, coordinates)
    coordinates = list(map(float, coordinates[0:2]))
    return {
      'name': stop,
      'location': coordinates
    }

  # Follow links from the initial URL to the pages for each stop
  def parse(self, response):
    # Links for all the stops
    stop_links = response.css('#leftColSub a::attr(href)').extract()
    # Parse the coordinates from each stop's page
    for stop_link in stop_links:
      next_page = response.urljoin(stop_link)
      yield scrapy.Request(next_page, callback=self.parse_coordinates)