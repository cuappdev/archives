from bs4 import BeautifulSoup
from lxml import html
import requests

lst = []
for i in range(5):
  page = requests.get('https://recreation.athletics.cornell.edu/fitness-centers/group-fitness-classes?&page=' + str(i)).text
  soup = BeautifulSoup(page, "lxml")

  schedule = soup.find_all("table")[1] # first table is irrelevant

  data = schedule.find_all("tr")[1:] # first row is header

  for row in data:
    current_row = []
    row_elems = row.find_all("td")
    current_row.append(row_elems[0].span.string)
    current_row.append(row_elems[1].span.string)
    current_row.append(row_elems[2].a.string)

    # special handling for time (cancelled)
    div = row_elems[3].span.div

    if div is not None:
      current_row.append(row_elems[3].span.div.span.string)
      current_row.append(row_elems[3].span.div.find_all("span")[1].string)
    else:
      current_row.append("Cancelled")
      current_row.append("Cancelled")

    current_row.append(row_elems[4].a.string)
    current_row.append(row_elems[5].a.string)
    lst.append(current_row)

print lst
