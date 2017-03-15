from openpyxl import load_workbook
from pprint import pprint

# Index into a sheet using row and col
def idx(row, col):
  return chr(ord('A')+col-1)+str(row)

# Test string for a value indicating end of processing
# Should eventually just be the test route (9900)
def is_end(s):
  return s != None and s.startswith("9900")


# Load the workbook as readonly to save memory space 
def load_schedule():
  wb = load_workbook(filename='tcat-schedule.xlsx', read_only=True)
  ws = wb["schedule"]
  return ws

#
def intermediate(ws):
  row = 1
  while (not is_end(ws[idx(row, 2)].value)):
    # Route number and name
    route = ws[idx(row, 2)].value
    # Route bound: Loop, Outbound, Inbound
    route_bound = ws[idx(row+1, 2)].value
    # Days that this route runs
    route_days = ws[idx(row+2,2)].value

    cols = 0

    # List of stops for
    route_stops = []
    while ws[idx(row+4, 3+cols)].value != None:
      route_stops.append(ws[idx(row+4, 3+cols)].value)
      cols += 1

    # The schedule for this route-bound-days tuple
    time_matrix = []
    time_rows = 0
    while ws[idx(row+5+time_rows, 3)].value != None:
      time_col = 0
      time_row = []
      while time_col < cols:
        time_row.append(ws[idx(row+5+time_rows, 3+time_col)].value)
        time_col += 1
      time_matrix.append(time_row)
      time_rows += 1

    # TODO: Implement scheduling aggregation for routes with outbound/inbound

    pprint(route)
    pprint(route_bound)
    pprint(route_days)
    pprint(route_stops)
    pprint(time_matrix)
    
    row += 6+time_rows

intermediate(load_schedule())