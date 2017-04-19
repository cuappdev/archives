from pprint import pprint
import data
import copy
import google
import getkml
from pprint import pprint
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3956 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def distance(a, b):
  loc = data.get_stops_mapped()[b]
  return haversine(a[0], a[1], loc[0], loc[1])

def find_subset(source, sink, start_time, trip):
  i = 0
  found = False
  while i < len(trip):
    (stop, bound, time) = trip[i]
    if stop == source and time >= start_time:
      found = True
      break
    i += 1

  # If no time availabe, then we are done
  if not found:
    return []

  # Find an end to the trip
  j = i + 1
  while j < len(trip):
    (stop, bound, time) = trip[j]
    if stop == source and j != i + 1:
      break
    j += 1


  subtrip = trip[i:j]
  min_index = 0
  for k in range(len(subtrip)):
    if distance(sink, subtrip[k][0]) < distance(sink, subtrip[min_index][0]):
      min_index = k
  return subtrip[i:min_index+1]


def raptor1(source, sink, sink_name, day, time):
  reduced_data = {}
  for route in data.get_data():
    for trip in route['trips']:
      if day in trip['days']:
        reduced_data[route['number']] = {
          'stops': trip['stops'],
          'trips': trip['trips']
        }
        break

  stopRoutes = {}
  for stop in data.get_stops_in_data():
    for (number, trip) in reduced_data.items():
      if stop in trip['stops']:
        if stop not in stopRoutes:
          stopRoutes[stop] = set([number])
        else:
          stopRoutes[stop].add(number)

  source_closest = list(data.get_stops_in_data())

  source_closest.sort(key=lambda x: distance(source, x))
  pprint(source_closest)

  trips = []
  for stop in source_closest:
    if stop in stopRoutes:
      for route in stopRoutes[stop]:
        trip = find_subset(stop, sink, time, reduced_data[route]['trips'][0])
        if trip != []:
          trips.append((route, trip))

  directions = []
  for (number, trip) in trips:
    walkToDirection = {
      'directionType':'walk',
      'place': trip[0][0],
      'location': source,
      'destinationLocation': data.get_stops_mapped()[trip[0][0]],
    }

    departDirection = {
      'directionType': 'depart',
      'place': trip[0][0],
      'location': data.get_stops_mapped()[trip[0][0]],
      'time': data.stringify_time(trip[0][2]),

      'routeNumber': number,
      'bound': trip[0][1],
      'stops': list(map(lambda x: x[0], trip)),
      'arrivalTime': data.stringify_time(trip[-1][2]),
      'kml': getkml.get_kml()[number].to_string()
    }

    arriveDirection = {
      'directionType': 'arrive',
      'place': trip[-1][0],
      'location': data.get_stops_mapped()[trip[-1][0]],
      'time': data.stringify_time(trip[-1][2]),
    }

    walkToDirection2 = {
      'directionType':'walk',
      'place': trip[-1][0],
      'location': data.get_stops_mapped()[trip[-1][0]],
      'destinationLocation': sink
    }

    directions.append({
      'directions':[
        walkToDirection,
        departDirection,
        arriveDirection,
        walkToDirection2
      ] ,

      'stopNames': departDirection['stops'],
      'stopNumbers': [number] * len(departDirection['stops'])
    })

  return directions