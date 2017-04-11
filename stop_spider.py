import scrapy
import re

class StopSpider(scrapy.Spider):
  name = "stops"
  start_urls = [
    'https://tcat.nextinsight.com/allstops.php'
  ]

  def parse_coordinates(self, response):
    stop = response.css('div.g1-hgroup h1::text').extract_first()
    coordinate = response.css('div.g1-inner li a::attr(href)')[3].extract()
    coordinates = list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", coordinate)[0:2]))
    return {
      stop: coordinates
    }

  def parse(self, response):
    stop_links = response.css('#leftColSub a::attr(href)').extract()
    # print(stop_links)
    for stop_link in stop_links:
      next_page = response.urljoin(stop_link)
      yield scrapy.Request(next_page, callback=self.parse_coordinates)