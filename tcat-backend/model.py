from dotaccess import Map
import convert

# Flatten a list of lists into a list
flatten = lambda l: [item for sublist in l for item in sublist]

# Represents a path of timepoints formed by a table
class Path:

  def __init__(self, number, table):
    # Retrieve basic information
    bound = table.bound
    stops = table.stops
    times = table.times

    # Form a path by adding rows of table in order
    timepoints = []
    n = len(times)
    m = len(stops)
    for i in range(n):
      for j in range(m):
        # Tuple of timepoint and index of timepoint
        timepoints.append((Map({
          'stop': stops[j], 
          'bound': bound[j], 
          'time': times[i][j],
          'number': number
        }), Map({
          'i': i,
          'j': j
        })))
    timepoints = list(filter(lambda x: x[0].time != -1, timepoints))
    unzipped = [list(t) for t in zip(*timepoints)]
    self.timepoints = unzipped[0]
    self.indexes = unzipped[1]


  # Get a trip servicing stop [start] at time [depart_time]
  def trip_from_stop_time(self, start, depart_time):
    n = len(self.timepoints)
    
    # Find a time for the start stop
    i = 0
    found = False
    while i < n:
      if self.timepoints[i].stop == start:
        if self.timepoints[i].time >= depart_time:
          found = True
          break
      i += 1

    # If no time availabe, then we are done
    if not found:
      return []

    # Find an end to the trip
    j = i + 1
    while j < n:
      if self.timepoints[j].stop == start:
        if self.indexes[j].i > self.indexes[i].i:
          if self.indexes[j].j >= self.indexes[i].j:
            break
      j += 1

    trip = self.timepoints[i:j]

    # Remove adjacent duplicates
    mark_dup = -1
    for i in range(len(trip) - 1):
      if trip[i].stop == trip[i + 1].stop:
        mark_dup = i
    if mark_dup != -1:
      _ = trip.pop(mark_dup)

    return trip

  # Get a trip servicing stop [start] at time [depart_time]
  def trip_to_stop_time(self, start, arrive_time):
    n = len(self.timepoints)
    
    # Find a time for the start stop
    i = 0
    found = False
    while i < n:
      if self.timepoints[i].stop == start:
        if self.timepoints[i].time >= arrive_time:
          break
      i += 1
    while i >= 0:
      if self.timepoints[i].stop == start:
        found = True
        break
      i -= 1

    # If no time availabe, then we are done
    if not found:
      return []

    # Find an end to the trip
    j = i - 1
    while j >= 0:
      if self.timepoints[j].stop == start:
        if self.indexes[j].i < self.indexes[i].i:
          if self.indexes[j].j <= self.indexes[i].j:
            break
      j -= 1

    trip = self.timepoints[j+1:i+1]

    # Remove adjacent duplicates
    mark_dup = -1
    for i in range(len(trip) - 1):
      if trip[i].stop == trip[i + 1].stop:
        mark_dup = i
    if mark_dup != -1:
      _ = trip.pop(mark_dup)

    return trip

# Represent a TCAT route
class Route:

  def __init__(self, route):
    # Extract simple information
    self.number = route.number
    all_stops = list(map(lambda x: x.stops, route.tables))
    self.stops = set(flatten(all_stops))
    self.days = [[]] * 7

    # Form paths out of table
    paths = list(map(lambda x: Path(route.number, x), route.tables))
    # Map paths to days
    for (table, path) in zip(route.tables, paths):
      first = min(table.days)
      last = max(table.days)
      for i in range(first, last+1):
        self.days[i].append(path)

  # Check if route has stop
  def has_stop(self, stop):
    return stop in self.stops

  def trips_from_stop_day_time(self, start, day, depart_time):
    trips = []
    for path in self.days[day]:
      trips.append(path.trip_from_stop_time(start, depart_time))
    return trips

  def trips_to_stop_day_time(self, start, day, arrive_time):
    trips = []
    for path in self.days[day]:
      trips.append(path.trip_to_stop_time(start, arrive_time))
    return trips