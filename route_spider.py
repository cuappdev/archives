import scrapy
import re

BOUND_ROW = 0
STOPS_ROW = 1
TIME_ROW = 4
FLOAT_REGEX = r"[-+]?\d*\.\d+|\d+"
DAYS_REGEX = r"Weekdays|Monday|Tueday|Wednesday|Thursday|Friday|Saturday|Sunday"
DAYS_INT_LOOKUP = {
  "Monday": 1,
  "Tueday": 2,
  "Wednesday": 3,
  "Thursday": 4,
  "Friday": 5,
  "Saturday": 6,
  "Sunday": 7
}

class RouteSpider(scrapy.Spider):
  name = "routes"
  start_urls = [
    'https://tcat.nextinsight.com/allroutes.php'
  ]

  def parse_table(self, header, table):
    days = []
    matches = re.findall(DAYS_REGEX, header)
    if matches == ['Weekdays']:
      days = [1, 5]
    elif len(matches) == 1:
      days = [DAYS_INT_LOOKUP[matches[0]], DAYS_INT_LOOKUP[matches[0]]]
    else:
      days = [DAYS_INT_LOOKUP[matches[0]], DAYS_INT_LOOKUP[matches[1]]]

    tr = table.css('tr')
    bound = tr[BOUND_ROW].css('td h6::text').extract_first().split()[0].lower()
    stops = tr[STOPS_ROW].css('td::text').extract()
    times = []
    for i in range(TIME_ROW, len(tr)):
      row_data = tr[i].css('td::text').extract()
      times.append(row_data)
    return {
      "bound": bound,
      "days": days,
      "stops": stops,
      "times": times
    }

  def parse_tables(self, response):
    number = response.css('h1.entry-title::text').extract_first()
    number = int(re.findall(FLOAT_REGEX, number)[0])
    headers = response.css('h5::text').extract()
    timetables = response.css('table')
    num_timetables = len(timetables)
    
    parsed_timetables = []
    for i in range(num_timetables):
      parsed_timetables.append(self.parse_table(headers[i], timetables[i]))

    return {
      "number": number,
      "timetables": parsed_timetables
    }


  def parse(self, response):
    route_links = response.css('div.entry-content a::attr(href)').extract()

    for route_link in route_links:
      next_page = response.urljoin(route_link)
      yield scrapy.Request(next_page, callback=self.parse_tables)