from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello, world!'

@app.route('/navigate')
def navigate():
  resp = {
    "departureTime": "7:21 PM",
    "arrivalTime": "7:39 PM",
    "timeUntilDeparture": 5,
    "directions": [{
      "directionType": "walk",
      "departureTime": "7:21 PM",
      "departurePlace": "Statler Hall",
      "travelDistance": 0.2
    },{
      "directionType": "board",
      "routeNumber": 32,
      "bound": "inbound",
      "stops": ["Bus Stop Name", "Bus Stop Name", "Bus Stop Name"],
      "departureTime": "7:24 PM",
      "departurePlace": "Statler Hall",
      "arrivalTime": "7:36 PM",
      "arrivalPlace": "Ithaca Commons",
      "travelTime": 12
    },{
      "directionType": "walk",
      "departureTime": "7:39 PM",
      "departurePlace": "Angry Mom Records",
      "travelDistance": 0.2
    }],
    "mainStops": ["Baker Flagpole", "Angry Mom Records"]
  }
  return jsonify(resp)

@app.route('/stops')
def stops():
  return jsonify([{"name": "Statler Hall", "number": 32}])

if __name__ == '__main__':
  app.run('0.0.0.0')