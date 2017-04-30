from dotaccess import Map
import json
import re


def time_int_to_string(time):
  m = 'AM'
  if time > 12 * 60:
    time -= 12 * 60
    m = 'PM'
  hours = time // 60
  minutes = time - 60 * hours
  if hours == 0:
    hours = 12
  return '{}:{:0>2} {}'.format(hours, minutes, m)

# Convert a time_string_to_int
def time_string_to_int(time):
  time_regex = r'\d+|AM|PM'
  components = re.findall(time_regex, time)
  if components == []: return -1
  hours = int(components[0])
  minutes = int(components[1])
  int_time = hours * 60 + minutes
  if hours == 12:
    int_time = minutes
  if components[2] == 'PM':
    int_time += 12 * 60
  return int_time

# Merge outbound and inbound tables to form a single1
def merge_tables(outbound, inbound):
  # Counters/limits for combining table rows
  i = 0
  j = 0
  n = len(outbound)
  # New set of merged tables
  tables = []

  # Perform merge operation for each matching pair of tables
  while i < n and j < n:
    # Left and right segments of new table
    left = outbound[i]
    right = inbound[j]
    # Move the right table up by 1 if it doesn't match
    if left.days != right.days:
      j += 1
      right = inbound[j]

    # Store bounds as a lambda function
    merged_bounds = [left.bound] * len(left.stops) + [right.bound] * len(right.stops)
    # Convert times to integers and merge the tables
    merged_times = []
    for k in range(len(left.times)):
      left_row = list(map(time_string_to_int, left.times[k]))
      right_row = list(map(time_string_to_int, right.times[k]))
      merged_times.append(left_row + right_row)

    i += 1
    j += 1
    tables.append(Map({
      'bound': merged_bounds,
      'days': left.days,   
      'stops': left.stops + right.stops,
      'times': merged_times
    }))

  return tables

# Convert the tables for a route
def convert_tables(tables):
  tables = list(map(lambda x: Map(x), tables))
  # Grab the tables for each possible bound
  loop_tables = list(filter(lambda x: x.bound == 'loop', tables))
  outbound_tables = list(filter(lambda x: x.bound == 'outbound', tables))
  inbound_tables = list(filter(lambda x: x.bound == 'inbound', tables))
  south_tables = list(filter(lambda x: x.bound == 'south', tables))
  north_tables = list(filter(lambda x: x.bound == 'north', tables))

  # Form new tables
  new_tables = []
  for table in loop_tables:
    # Quick conversion of loop tables
    new_tables.append(Map({
          'bound': [table.bound] * len(table.stops),
          'days': table.days,   
          'stops': table.stops,
          'times': list(map(lambda x: list(map(time_string_to_int, x)), table.times))
        }))
  new_tables += merge_tables(outbound_tables, inbound_tables)
  new_tables += merge_tables(south_tables, north_tables)
  return new_tables


# Convert the routes into a human readable form
def convert(filename):
  with open(filename) as data_file:
    data = json.load(data_file)
    new_data = []
    for route in data:
      route = Map(route)
      # Route 17 has some really awkward formatting, to be handled later
      if route.number not in [10, 17]:
        new_data.append(Map({
          'number': route.number, 
          'tables': convert_tables(route.tables)
        }))
    return new_data