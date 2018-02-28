from bs4 import BeautifulSoup
from lxml import html
import requests

BASE_URL = "https://recreation.athletics.cornell.edu"


"""
Scrape class descrption from [class_href]
"""
def scrape_class(class_href):
    page = requests.get(BASE_URL + class_href).text
    soup = BeautifulSoup(page, "lxml")
    contents = soup.find(
        'div',
        {'class': 'taxonomy-term-description'}
    ).p.contents

    description = ""
    for c in contents:
      if isinstance(c, basestring):
        description += c
      else:
        try:
          description += c.string
        except:
          break
    return description

"""
Scrape classes from the group-fitness-classes page
Params:
  num_pages: number of pages to scrape
Returns:
  list of classes, dictionary of class descriptions
"""
def scrape_classes(num_pages):
  lst = []
  classes = {}

  for i in range(num_pages):
    page = requests.get(
        BASE_URL + '/fitness-centers/group-fitness-classes?&page=' + str(i)
    ).text
    soup = BeautifulSoup(page, "lxml")

    schedule = soup.find_all("table")[1] # first table is irrelevant

    data = schedule.find_all("tr")[1:] # first row is header

    for row in data:
      current_row = []
      row_elems = row.find_all("td")
      current_row.append(row_elems[0].span.string)
      current_row.append(row_elems[1].span.string)
      current_row.append(row_elems[2].a.string)

      class_href = row_elems[2].a["href"]
      if class_href not in classes:
        classes[class_href] = scrape_class(class_href)

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
  return lst, classes

if __name__ == "__main__":
  print(scrape_classes(1))
