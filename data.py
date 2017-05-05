from dotaccess import Map
import json
import convert
from model import *
import re

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
    with open('data\\stops.json') as stops_file:
      _stops = json.load(stops_file)
      _stops = list(map(lambda x: Map(x), _stops))
  
  # Load data from disk, convert it, and use the model
  if _routes == None:
    _routes = convert.convert('data\\routes.json')
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
    with open('data\\kml.json') as kml_file:
      _all_kml = json.load(kml_file)
      _all_kml = list(map(lambda x: Map(x), _all_kml))

def stops():
  load()
  global _stops
  return _stops

def routes():
  load()
  global _routes
  return _routes

def kml_for_number(number):
  load()
  global _all_kml
  for kml in _all_kml:
    if kml.number == number:
      return kml.placemark
  return None

def stops_in_routes():
  load()
  global _stops_in_routes
  return _stops_in_routes

def routes_for_stop(stop):
  load()
  global _stops_to_routes
  return _stops_to_routes[stop]

def location_from_stop(stop):
  load()
  global _stops
  for s in _stops:
    if s.name == stop:
      return s.location
  return None