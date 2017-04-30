from pprint import pprint
from dotaccess import Map
import data
import copy
# import google

lookup = None
num_rounds = 1

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

"""

def compute_journeys(start, stop, depart_time, arrival_time):
  if arrival_time != 2400:
    return compute_journeys_inverse(start, stop, depart_time, arrival_time)

   

def compute_journeys_inverse(start, stop, depart_time, arrival_time) 

"""