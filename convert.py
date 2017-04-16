from dot import Map
import json

# Convert a time_string_to_int
def time_string_to_int(time):
  time_regex = r'\d+|AM|PM'
  components = re.findall(time_regex, time)
  if components == []: return -1
  hours = int(components[0])
  minutes = int(components[1])
  int_time = hours * 60 + minutes
  if components[2] == 'PM':
    int_time += 12 * 60
  return int_time

def merge_tables(tables1, tables2, forward, backward):
  pass

# Convert tables to "paths", marked with times and bounds
def convert_table(table):
  # Pull data from the table
  days = list(range(table.days[0], table.days[1]+1))
  bound = table.bound
  stops = table.stops
  # Convert the times to integers
  map_function = lambda x: list(map(time_string_to_int, x))
  times = list(map(map_function, table.times))
  
  # Paths dictated by the table
  paths = [[]]
  i = 0
  n = 1
  m = len(stops)
  while times != []:
    # In case of Route 10 and a few others
    # times do not flow directly to the next row
    if i == 1:
      (_, _, last_time) = paths[0][-1]
      if times[0][0] < last_time:
        paths.append([])
        n += 1
    # Add to path, leaving out stops without times
    for j in range(m):
      item = (stops[j], bound, times[0][j])
      if not isinstance(bound, str):
        item = (stops[j], bound(j), times[0][j])
      if times[0][j] != -1:
        path[i % n].append(item)
    i += 1
    _ = times.pop(0)

# Convert the tables for a route
def convert_tables(tables):
  tables = map(lambda x: Map(x), tables)
  # Grab the tables for each possible bound
  loop_tables = filter(lambda x: x.bound == 'loop', tables)
  outbound_tables = filter(lambda x: x.bound == 'outbound', tables)
  inbound_tables = filter(lambda x: x.bound == 'inbound', tables)
  south_tables = filter(lambda x: x.bound == 'south', tables)
  north_tables = filter(lambda x: x.bound == 'north', tables)

# Convert the routes into a human readable form
def convert(filename):
  with open(filename) as data_file:
    data = json.load(data_file)
    for route in data:
      route = Map(route)
      # Route 17 has some really awkward formatting, to be handled later
      if route.number != 17
        convert_tables(route.tables)