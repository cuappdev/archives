from openpyxl import load_workbook

# REDO ALL STRUCTURE

def index(idxl, idxr):
  return chr(ord('A')+idxl-1)+str(idxr)

def is_test_route(s):
  return s != None and s.startswith("9900")

wb = load_workbook(filename='schedule.xlsx', read_only=True)
ws = wb["schedule"]

row = 1

def parse():
  while (not is_test_route(ws[index(2, row)].value)):
    route = ws[index(2,row)].value
    route_type = ws[index(2, row+1)].value
    route_day = ws[index(2, row+2)].value

    route_stops = []
    
    cols = 0
    while ws[index(3 + cols, row+4)].value != None:
      route_stops.append(ws[index(3 + cols, row+4)].value)
      cols += 1

    time_matrix = []
    time_rows = 0
    while ws[index(3, row+5+time_rows)].value != None:
      time_col = 0
      time_row = []
      while time_col < cols:
        time_row.append(ws[index(3 + time_col, row+5+time_rows)].value)
        time_col += 1
      time_matrix.append(time_row)
      time_rows += 1

    #print(route)
    #print(route_type)
    #print(route_day)
    #print(route_stops)
    #print(time_matrix)
    row += 6 + time_rows