from dot import Map
import json
import convert
from model import *
from fastkml import kml
import re

<<<<<<< HEAD
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
=======
# List of stops and their locations
_stops = None
# List of routes
_routes = None
# Set of stops in the routes
_stops_in_routes = None
# Mapping of stops to routes they are part of
_stops_to_routes = None
# All kml for the stops
_all_kml = None

# Load all the data
def load():
  global _stops
  global _routes
  global _stops_in_routes
  global _stops_to_routes
  global _all_kml
  # Load stops from disk
  if _stops == None:
    with open('stops.json') as stops_file:
      _stops = json.load(stops_file)
      _stops = list(map(lambda x: Map(x), _stops))
  
  # Load data from disk, convert it, and use the model
  if _routes == None:
    _routes = convert.convert('data.json')
    _routes = list(map(lambda x: Route(x), _routes))

  # Process routes for stops
  if _stops_in_routes == None:
    _stops_in_routes = set()
    for route in _routes:
      _stops_in_routes = _stops_in_routes | route.stops
  
  # Process stops in routes and stops to get stuff done
  if _stops_to_routes == None:
    _stops_to_routes = {}
    for stop in _stops_in_routes:
      _stops_to_routes[stop] = []
    for stop in _stops_in_routes:
      for route in _routes:
        if stop in route.stops:
          _stops_to_routes[stop].append(route)

  # Load kml
  if _all_kml == None:
    _all_kml = {}
    k = kml.KML()
    with open('tcat-routes.kml') as f:
      k.from_string(f.read())
    features = list(k.features())
    f2 = list(features[0].features())
    for i in range(len(f2)):
      f3 = list(f2[i].features())
      for j in range(len(f3)):
        for f4 in f3[j].features():
          number = int(re.findall(r'\d+', f4.name)[0])
          _all_kml[number]=f4

def stops():
  load()
  global stops
  return stops
>>>>>>> origin/unstable

def routes():
  load()
  global routes
  return routes

def all_kml():
  load()
  global _all_kml
  return _all_kml

def stops_in_routes():
  load()
  global stops_in_routes
  return stops_in_routes

def routes_for_stop(stop):
  load()
  global stops_to_routes
  return stops_to_routes[stop]

def location_from_stop(stop):
  load()
  global stops
  for s in stops:
    if s.name == stop:
      return s.location
  return None