from flask import Flask, jsonify, request
import json
import data
import raptor
import datetime
import google
import re

application = app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello, world!'

@app.route('/navigate')
def navigate():
  source = request.args.get('source')
  sink = request.args.get('sink')
  
  source_location = list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", source)[0:2]))
  sink_match = re.match(r"[-+]?\d*\.\d+|\d+,[-+]?\d*\.\d+|\d+", sink)
  sink_location = []
  if sink_match != None:
    sink_location = list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", sink)[0:2]))
  else:
    (sink_location, sink_name) = google.get_coordinates(sink)

  print("{} {}".format(source_location, sink_location))

  now = datetime.datetime.now()
  midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
  time = (now - midnight).seconds // 60 - 300
  day = datetime.datetime.today().weekday() + 1

  return jsonify(raptor.raptor1(source_location, sink_location, '', day, time))

@app.route('/stops')
def stops():
  return jsonify(data.get_stops())

if __name__ == '__main__':
  application.run(host='0.0.0.0', debug=True)  