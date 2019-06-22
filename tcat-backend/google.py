import requests

PLACES_API_KEY='AIzaSyAIZ2A5zNPU9IRZU2lyCMELkYVb_bnnY6k'
DISTANCE_MATRIX_API_KEY='AIzaSyBxfkH3rkuQJjF8h3Qq9EN5DDBAp_WyQYQ'

def get_coordinates(place_id):
  parameters = {'key': PLACES_API_KEY, 'placeid': place_id}
  response = requests.get('https://maps.googleapis.com/maps/api/place/details/json', params=parameters)
  j = response.json()
  location = j['result']['geometry']['location']
  return ([location['lat'], location['lng']], j['result']['name'])
