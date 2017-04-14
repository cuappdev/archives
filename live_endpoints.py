from flask import Flask, jsonify
import json
import data
import raptor
import datetime

app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello, world!'

@app.route('/navigate')
def navigate():
  source = request.args.get('source')
  sink = request.args.get('sink')
  (source_location, _) = google.get_coordinates(source)
  (sink_location, sink_name) = google.get_coordinates(sink)

  now = datetime.datetime.now()
  midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
  time = (now - midnight).seconds // 60
  day = datetime.datetime.today().weekday() + 1

  return jsonify(raptor.raptor1(source_location, sink_location, sink_name, day, time))

@app.route('/stops')
def stops():
  return jsonify(data.get_stops())

if __name__ == '__main__':
  app.run('0.0.0.0')  