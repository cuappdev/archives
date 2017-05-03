from flask import Flask, jsonify, request
import json
import data
import convert
import raptor
import datetime
import google
import re

application = Flask(__name__)

@application.route('/')
def hello_world():
  return 'Hello, world!'

@application.route('/navigate')
def navigate():
  data.load()
  source = request.args.get('source')
  sink = request.args.get('sink')
  depart_time = request.args.get('depart_time')

  source_location = convert.lat_lng_string_to_list(source)
  source_name = source
  if source_location == None:
    (source_location, source_name) = google.get_coordinates(source)

  sink_location = convert.lat_lng_string_to_list(sink)
  sink_name = sink
  if sink_location == None:
    (sink_location, sink_name) = google.get_coordinates(sink)

  if depart_time != None:
    now = datetime.datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    time = (now - midnight).seconds // 60
    time = depart_time
  
  day = datetime.datetime.today().weekday()

  journeys = raptor.compute_journeys(
      source_location, 
      sink_location, 
      sink_name, 
      day, 
      time
    )
  return jsonify()

@application.route('/stops')
def stops():
  return jsonify(data.get_stops())

if __name__ == '__main__':
  application.run()  