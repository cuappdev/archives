from dot import Map
import json
import convert
from model import *

# List of stops and their locations
_stops = None
# List of routes
_routes = None
# Set of stops in the routes
_stops_in_routes = None
# Mapping of stops to routes they are part of
_stops_to_routes = None

# Load all the data
def load():
  global _stops
  global _routes
  global _stops_in_routes
  global _stops_to_routes
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


def stops():
  load()
  global stops
  return stops

def routes():
  load()
  global routes
  return routes

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