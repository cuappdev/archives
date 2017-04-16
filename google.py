import requests

PLACES_API_KEY='AIzaSyAIZ2A5zNPU9IRZU2lyCMELkYVb_bnnY6k'
DISTANCE_MATRIX_API_KEY='AIzaSyBxfkH3rkuQJjF8h3Qq9EN5DDBAp_WyQYQ'

def get_coordinates(place_id):
  parameters = {'key': PLACES_API_KEY, 'placeid': place_id}
  response = requests.get('https://maps.googleapis.com/maps/api/place/details/json', params=parameters)
  j = response.json()
  print(j)
  location = j['result']['geometry']['location']
  return ([location['lat'], location['lng']], j['result']['name'])

def get_distance_time(loc1, loc2):
  parameters = {
    'key': DISTANCE_MATRIX_API_KEY, 
    'origins': "{},{}".format(loc1[0], loc1[1]),
    'destinations': "{},{}".format(loc2[0], loc2[1]),
    "mode": "walking"
  }
  response = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json', params=parameters)
  j = response.json()
  distance = j['rows'][0]['elements'][0]['distance']['value']
  distance *= 0.000621371
  time = j['rows'][0]['elements'][0]['duration']['value']
  time = time // 60
  return (distance, time)