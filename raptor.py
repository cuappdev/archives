import json
from pprint import pprint
import re

TIME_REGEX = r'\d+|AM|PM'

def intify_time(time):
  components = re.findall(TIME_REGEX, time)
  if components == []: return -1
  hours = int(components[0])
  minutes = int(components[1])
  int_time = hours * 60 + minutes
  if components[2] == 'PM':
    int_time += 12 * 60
  return int_time 

def intify_timetable(times):
  return list(map(lambda x: list(map(intify_time, x)), times))


def rangify_days(days):
  return list(range(days[0], days[1]+1))

def merge_timetables(route):
  timetables = route['timetables']
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

def load_data():
  with open('data.json') as data_file:
    data = json.load(data_file)
    raptorfied_data = []
    for route in data:
      if route['number'] != 17:
        route['timetables'] = merge_timetables(route)

        raptorfied_data.append(route)
    return raptorfied_data
  return None

pprint(load_data())
