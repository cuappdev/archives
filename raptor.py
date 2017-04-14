from pprint import pprint
import data
import copy
import google
import getkml

def distance(a, b):
  loc = data.get_stops_mapped()[b]
  return (a[0] - loc[0])**2 + (a[1] - loc[1])**2

def find_subset(source, start_time, trip):
  subset = []
  i = 0
  #pprint(trip[i])
  (stop, bound, time) = trip[i]
  while stop != source and time <= start_time:
    i += 1
    (stop, bound, time) = trip[i]

  j = i + 1
  (stop, bound, time) = trip[j]
  if stop == source:
    j = j + 1
  while stop != source and j < len(trip):
      (stop, bound, time) = trip[j]
      j += 1
  return trip[i:j+1]

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

  trips = []
  for stop in source_closest:
    if stop in stopRoutes:
      for route in stopRoutes[stop]:
        trip = find_subset(stop, time, reduced_data[route]['trips'][0])
        trip = list(filter(lambda x: x[2] != -1, trip))
        if trip != []:
          trips.append((route, trip))

  sorted_trips = []
  for trip in trips:
    sorted_trip = copy.deepcopy(trip)
    sorted_trip[1].sort(key=lambda x: distance(sink, x[0]))
    sorted_trips.append(sorted_trip)

  trip = min(sorted_trips, key=lambda x: x[1][0][2])
  trip[1].sort(key=lambda x: x[2 ])
  (number, trip) = trip

  (distance1, time1) = google.get_distance_time(source, data.get_stops_mapped()[trip[0][0]])
  (distance2, time2) = google.get_distance_time(data.get_stops_mapped()[trip[-1][0]], sink)

  walkToDirection = {
    'directionType':'walk',
    'place': trip[0][0],
    'location': data.get_stops_mapped()[trip[0][0]],
    'time': data.stringify_time(trip[0][2] - time1),
    'travelDistance': distance1
  }

  departDirection = {
    'directionType': 'depart',
    'place': trip[0][0],
    'location': data.get_stops_mapped()[trip[0][0]],
    'time': data.stringify_time(trip[0][2]),

    'routeNumber': number,
    'bound': trip[0][1],
    'stops': list(map(lambda x: x[0], trip)),
    'arrivalTime': data.stringify_time(trip[-1][2])
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
    'location': sink_name,
    'time': data.stringify_time(trip[-1][2] + time2),
    'travelDistance': distance2
  }

  return {
    'departureTime': walkToDirection['time'],
    'arrivalTime': walkToDirection2['time'],

    'directions':[
      walkToDirection,
      departDirection,
      arriveDirection,
      walkToDirection2
    ] ,

    'stopNames': departDirection['stops'],
    'stopNumbers': [number] * len(departDirection['stops'])
  }