import json
from pprint import pprint
import re
from functools import reduce

TIME_REGEX = r'\d+|AM|PM'

data = None
stops = None
stops_mapped = None
stops_in_data = None

def stringify_time(time):
  if time < 0:
    time += 24 * 60
  m = 'AM'
  if time > 12 * 60:
    time -= 12 * 60
    m = 'PM'
  hours = time // 60
  minutes = time - 60 * hours
  if hours == 0:
    hours = 12
  return '{}:{:0>2} {}'.format(hours, minutes, m)

def intify_time(time):
  components = re.findall(TIME_REGEX, time)
  if components == []: return -1
  hours = int(components[0])
  if hours == 12:
    hours = 0
  minutes = int(components[1])
  int_time = hours * 60 + minutes
  if components[2] == 'PM':
    int_time += 12 * 60
  return int_time 

def intify_timetable(times):
  return list(map(lambda x: list(map(intify_time, x)), times))


def rangify_days(days):
  return list(range(days[0], days[1]+1))

def merge_timetables(timetables):
  merged_tables = []

  i = 0
  while i < len(timetables):
    table = timetables[i]
    if table['bound'] in ['loop', 'inbound', 'north']:
      merged_table = {
        'days': rangify_days(table['days']),
        'bound': lambda x: table['bound'], 
        'stops': table['stops'], 
        'times': intify_timetable(table['times']) 
      }
      merged_tables.append(merged_table)
      i += 1
      continue

    if table['bound'] in ['outbound', 'south']:
      next_table = timetables[i + 1]
      stops1 = table['stops']
      stops2 = next_table['stops']
      merged_stops = stops1 + stops2
      # TODO: Support south bound and north bound
      merged_bounds = lambda x: 'outbound' if x in list(range(len(stops1))) else 'inbound'

      times1 = table['times']
      times2 = next_table['times']
      merged_times = []
      for j in range(len(times1)):
        merged_times.append(times1[j] + times2[j])

      merged_table = {
        'days': rangify_days(table['days']),
        'bound': merged_bounds,
        'stops': merged_stops,
        'times': intify_timetable(merged_times)
      }

      merged_tables.append(merged_table)
      i += 2
      continue

    print("Should not reach this case for route {}".format(route['number']))

  return merged_tables

def flatten_timetable(timetable):
  bounds = timetable['bound']
  stops = timetable['stops']
  times = timetable['times']
  flattened_times = [[]]
  i = 0
  rows = 1
  while times != []:
    if i == 1:
      (_, _, last_time) = flattened_times[0][-1]
      if times[0][0] < last_time:
        flattened_times.append([])
        rows += 1
    for j in range(len(stops)):
      stop_bound = bounds(j)
      item = (stops[j], stop_bound, times[0][j])
      flattened_times[i % rows].append(item)
    i += 1
    _ = times.pop(0)

  return {
    'days': timetable['days'],
    'stops': set(stops),
    'trips': flattened_times
  }

def load_data():
  with open('data.json') as data_file:
    data = json.load(data_file)
    raptorfied_data = []
    stops = []
    for route in data:
      if route['number'] != 17:
        trips = merge_timetables(route['timetables'])
        for trip in trips:
          stops = stops + trip['stops']
        trips = list(map(flatten_timetable, trips))
        raptorfied_data.append({
          'number': route['number'],
          'trips': trips
        })
    global stops_in_data
    stops_in_data = set(stops)
    return raptorfied_data
  return None

def get_data():
  global data
  if data == None:
    data = load_data()
  return data

def get_stops():
  global stops
  if stops == None:
    with open('stops2.json') as stops_file:
      stops = json.load(stops_file)
  return stops

def get_stops_mapped():
  global stops_mapped
  if stops_mapped == None:
    stops_mapped = {}
    stops = get_stops()
    for stop in stops:
      stops_mapped[stop['name']] = stop['location']
  return stops_mapped

def get_stops_in_data():
  global stops_in_data
  if stops_in_data == None:
    get_data()
  return stops_in_data