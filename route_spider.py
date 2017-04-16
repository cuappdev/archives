import scrapy
import re

class RouteSpider(scrapy.Spider):

  # Regex for days of the week
  days_regex = r'Weekdays|Monday|Tueday|Wednesday|Thursday|Friday|Saturday|Sunday'
  # Map the days of the week to integer values
  days_to_int = {
    "Monday": 0,
    "Tueday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6
  }

  name = "routes"
  start_urls = [
    # URL for the list of all TCAT routes
    'https://tcat.nextinsight.com/allroutes.php'
  ]

  # Parse a table into a Python data structure
  def parse_table(self, header, table):
    # Parse the days this table applies to
    days = []
    # Find matches in the days of the week
    matches = re.findall(RouteSpider.days_regex, header)
    # Create "interval" list indicating days, ends inclusive
    if matches == ['Weekdays']:
      days = [0, 4]
    elif len(matches) == 1:
      days = [
        RouteSpider.days_to_int[matches[0]], 
        RouteSpider.days_to_int[matches[0]]
      ]
    else:
      days = [
        RouteSpider.days_to_int[matches[0]], 
        RouteSpider.days_to_int[matches[1]]
      ]

    # Grab all table rows
    tr = table.css('tr')
    # Grab the bound
    bound = tr[0].css('td h6::text').extract_first().split()[0].lower()
    # Grab the stops in the table
    stops = tr[1].css('td::text').extract()
    
    # Parse the times in the table
    times = []
    for i in range(4, len(tr)):
      row_data = tr[i].css('td::text').extract()
      times.append(row_data)
    return {
      "bound": bound,
      "days": days,
      "stops": stops,
      "times": times
    }

  # Parse the time tables for a route
  def parse_tables(self, response):
    # Get the route number
    number = response.css('h1.entry-title::text').extract_first()
    number = int(re.findall(r"\d+", number)[0])
    # Get the headers for each table
    headers = response.css('h5::text').extract()
    # Get each table
    tables = response.css('table')
    
    # Parse each table into a Python data structure
    n = len(tables)
    parsed_tables = []
    for i in range(n):
      parsed_tables.append(self.parse_table(headers[i], tables[i]))

    return {
      'number': number,
      'tables': parsed_tables
    }


  # Parse the time tables for each route
  def parse(self, response):
    # Get links to all the the route page
    route_links = response.css('div.entry-content a::attr(href)').extract()
    # Parse each page for the route and its time tables
    for route_link in route_links:
      next_page = response.urljoin(route_link)
      yield scrapy.Request(next_page, callback=self.parse_tables)