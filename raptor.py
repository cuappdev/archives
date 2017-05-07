from pprint import pprint
from dotaccess import Map
import data
import convert
import copy
from math import radians, cos, sin, asin, sqrt
# import google

num_rounds = 1


def haversine(lon1, lat1, lon2, lat2):

    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3956 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def distance(a, b):
  loc = data.location_from_stop(b)
  return haversine(a[0], a[1], loc[0], loc[1])

def raptor(start, day, depart_time):
  
  global num_transfers
  marked_stops = { start }
  journeys = [Map({}) for i in range(num_rounds)]

  for k in range(num_rounds):
    Q = set([])
    for stop in marked_stops:
      for route in data.routes():
        if route.has_stop(stop):
          Q.add((route, stop))
    marked_stops.remove(stop)

    if k == 0:
      for (route, stop) in Q:
        trips = route.trips_from_stop_day_time(stop, day, depart_time)
        for trip in trips:
          for i in range(1, len(trip)):
            if trip[i].stop not in journeys[k]:
              journeys[k][trip[i].stop] = trip[0:i+1]
              marked_stops.add(stop)
            elif journeys[k][trip[i].stop][-1].time > trip[i].time:
              journeys[k][trip[i].stop] = trip[0:i+1]
              marked_stops.add(stop)
    else:
      for (route, stop) in Q:
        trips = route.trips_from_stop_day_time(stop, day, journeys[k-1][stop][-1].time)
        for trip in trips:
          for i in range(1, len(trip)):
            if trip[i].stop not in journeys[k]:
              journeys[k][trip[i].stop] = journeys[k-1][stop] + trip[0:i+1]
              marked_stops.add(stop)
            elif journeys[k][trip[i].stop][-1].time > trip[i].time:
              journeys[k][trip[i].stop] = journeys[k-1][stop] + trip[0:i+1]
              marked_stops.add(stop)

  return journeys[-1]

def inverse_raptor(start, day, arrive_time):
  global num_transfers
  marked_stops = { start }
  journeys = [Map({}) for i in range(num_rounds)]

  for k in range(num_rounds):
    Q = set([])
    for stop in marked_stops:
      for route in data.routes():
        if route.has_stop(stop):
          Q.add((route, stop))
    marked_stops.remove(stop)

    if k == 0:
      for (route, stop) in Q:
        trips = route.trips_to_stop_day_time(stop, day, arrive_time)
        for trip in trips:
          for i in range(len(trip)-1, -1, -1):
            if trip[i].stop not in journeys[k]:
              journeys[k][trip[i].stop] = trip[i:len(trip)]
              marked_stops.add(stop)
            elif journeys[k][trip[i].stop][-1].time < trip[i].time:
              journeys[k][trip[i].stop] = trip[i:len(trip)]
              marked_stops.add(stop)
    else:
      for (route, stop) in Q:
        trips = route.trips_from_stop_day_time(stop, day, journeys[k-1][stop][0].time)
        for trip in trips:
          for i in range(len(trip)-1, -1, -1):
            if trip[i].stop not in journeys[k]:
              journeys[k][trip[i].stop] = trip[i:len(trip)] + journeys[k-1][stop] 
              marked_stops.add(stop)
            elif journeys[k][trip[i].stop][-1].time < trip[i].time:
              journeys[k][trip[i].stop] = trip[i:len(trip)] + journeys[k-1][stop]
              marked_stops.add(stop)

  return journeys[-1]

def format_output(source, sink, sink_name, depart_time, trip):
  directions = []
  directions.append({
      'directionType':'walk',
      'place': trip[0].stop,
      'location': source,
      'destinationLocation': data.location_from_stop(trip[0].stop),
    })
  i = 0

  while i < len(trip) - 1:
    if trip[i].number != trip[i+1].number:
      break
    i += 1
  
  stopNumbers = []
  if i != len(trip) - 1:
    directions.append({
        'directionType': 'depart',
        'place': trip[0].stop,
        'location': data.location_from_stop(trip[0].stop),
        'departureTime': convert.time_int_to_string(trip[0].time),

        'routeNumber': trip[0].number,
        'bound': trip[0].bound,
        'stops': list(map(lambda x: x.stop, trip[0:i+1])),
        'arrivalTime': convert.time_int_to_string(trip[i].time),
        'kml': data.kml_for_number(trip[0].number)
      })
    directions.append({
        'directionType': 'arrive',
        'place': trip[i].stop,
        'location': data.location_from_stop(trip[i].stop),
        'arrivalTime': convert.time_int_to_string(trip[i].time)
      })
    stopNumbers.append(trip[0].number)
    directions.append({
        'directionType': 'depart',
        'place': trip[i+1].stop,
        'location': data.location_from_stop(trip[i+1].stop),
        'departureTime': convert.time_int_to_string(trip[i+1].time),

        'routeNumber': trip[i+1].number,
        'bound': trip[i+1].bound,
        'stops': list(map(lambda x: x.stop, trip[i+1:len(trip)])),
        'arrivalTime': convert.time_int_to_string(trip[-1].time),
        'kml': data.kml_for_number(trip[i+1].number)
      })
    directions.append({
        'directionType': 'arrive',
        'place': trip[-1].stop,
        'location': data.location_from_stop(trip[-1].stop),
        'arrivalTime': convert.time_int_to_string(trip[-1].time)
      })
    stopNumbers.append(trip[i+1].number)
  else:
    directions.append({
        'directionType': 'depart',
        'place': trip[0].stop,
        'location': data.location_from_stop(trip[0].stop),
        'departureTime': convert.time_int_to_string(trip[0].time),

        'routeNumber': trip[0].number,
        'bound': trip[0].bound,
        'stops': list(map(lambda x: x.stop, trip)),
        'arrivalTime': convert.time_int_to_string(trip[-1].time),
        'kml': data.kml_for_number(trip[0].number)
      })
    directions.append({
        'directionType': 'arrive',
        'place': trip[-1].stop,
        'location': data.location_from_stop(trip[-1].stop),
        'arrivalTime': convert.time_int_to_string(trip[-1].time)
      })
    stopNumbers.append(trip[0].number)
  directions.append({
      'directionType':'walk',
      'place': sink_name,
      'location': data.location_from_stop(trip[-1].stop),
      'destinationLocation': sink,
    })
  stopNumbers.append(-1)
  return {
    'allStopNames': list(map(lambda x: x.stop, trip)),
    'mainStopNames': [trip[0].stop, trip[-1].stop] + [sink_name],
    'stopNumbers': stopNumbers,
    'directions': directions
  }

def compute_journeys(source, sink, sink_name, day, depart_time):
  source_closest = list(data.stops_in_routes())
  source_closest.sort(key=lambda x: distance(source, x))
    
  trips = []
  for stop in source_closest[0:7]:
    journeys = raptor(stop, day, depart_time)
    sink_closest = list(journeys.keys())
    sink_closest.sort(key=lambda x: distance(sink, x))
    for stop2 in sink_closest[0:7]:
      trips.append(journeys[stop2])

  trips.sort(key=lambda x: x[-1].time)
  return list(map(lambda x: format_output(source, sink, sink_name, depart_time, x), trips))

