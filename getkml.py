from fastkml import kml
import re

all_kml = None

def get_kml():
  global all_kml
  if all_kml == None:
    all_kml = {}
    k = kml.KML()
    with open('tcat-routes.kml') as f:
      k.from_string(f.read())
    features = list(k.features())
    f2 = list(features[0].features())
    for i in range(len(f2)):
      f3 = list(f2[i].features())
      for j in range(len(f3)):
        for f4 in f3[j].features():
          number = int(re.findall(r'\d+', f4.name)[0])
          print(number)
          all_kml[number]=f4
  return all_kml