# TCAT Backend (WIP)

This is the backend implementation of the TCAT app. Currently a work in progress, it will use TCAT scheduling data to calculate a route between two destinations using the TCAT bus system. It is built using Python 3.

Install:
1. Install the Python library `virtualenv`

   `pip install virtualenv`

2. Open a terminal in this project's directory and create a virtual environment `venv`

   `virtualenv venv`

3. Enter your virtual environment

   Windows:    `venv\Scripts\activate`
   Unix/Linux: `venv/bin/activate`
   
   You should see "(venv)" appear at the beginning of your terminal prompt. This means you have successfully entered the virtual environment, and any further `pip` and `python` commands will be self-contained and not affect your global install

3. Install the requisite Python libraries using the given `requirements.txt`

   pip install -r requirements.txt

4. Start the server to access endpoints

   python endpoints.py

5. To exit your virtual environment

   `deactivate`

Endpoints:
1. GET /

   "Hello, world!"

2. GET /navigate

   Calculates and returns a route using the TCAT bus system between a source and a destination

   Requires: 
   * `source` - a latitude-longitude pair indicating the start of the route
   * `sink`- a latitude-longitude pair indicating the destination of the route.
   * `area`- a general area for the destination of the route.

   Use only one of `sink` or `area` to indicate a destination. If both are supplied, only `sink` will be considered as the destination.

   Returns:
   * A list containing steps of a route. The encoding of the route is determined by the iOS models of the route.

   Currently returns a dummy route.

3. GET /stops

   Returns a list of stops, where each stop includes:
   * stop name
   * routes that it is a part of

   Currently returns a list of dummy stops

Roadmap:
1. Study and implement the RAPTOR algorithm (see `raptor_alenex.pdf` for more details)
2. Gather latitude-longitudes for stops and implement routing between lat-longs as a reduction to RAPTOR
3. Add "area" specialization for routing

Considerations:
1. We may have TCAT's GTFS data on-hand next month. If so, we would immediately switch over to using that as our backend data.