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


    "directions": [{
      "directionType": "walk",
      "time": "7:21 PM",
      "place": "Statler Hall",
      "location": [42.4446, 76.4823],

      "travelDistance": 0.2
    },{
      "directionType": "depart",
      "time": "7:24 PM",
      "place": "Statler Hall",
      "location": [42.4446, 76.4823],

      "routeNumber": 32,
      "bound": "inbound",
      "stops": ["Statler Hall", "Ithaca Commons"],
      "arrivalTime": "7:36 PM",
    }
    ,{
      "directionType": "arrive",
      "time": "7:36 PM",
      "place": "Ithaca Commons",
      "location": [42.4396, 76.4970]
    },{
      "directionType": "walk",
      "time": "7:39 PM",
      "place": "Angry Mom Records",
      "location": [42.4393, 76.4982],
      
      "travelDistance": 0.2
    }],
    "stopNames": ["Statler Hall", "Ithaca Commons"],
    "stopNames": [32, 32]
  }
  return jsonify(resp)

@app.route('/stops')
def stops():
  return jsonify([{"name": "Statler Hall", "numbers": [32]}, {"name": "Ithaca Commons", "numbers": [32]}])

if __name__ == '__main__':
  app.run('0.0.0.0')