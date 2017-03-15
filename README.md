# TCAT Backend (WIP)

This is the backend implementation of the TCAT app. Currently a work in progress, it will use TCAT scheduling data to calculate a route between two destinations using the TCAT bus system. It is built using Python 3.

Install:
1. Install the Python library `virtualenv`

   `pip install virtualenv`

2. Open a terminal in this project's directory and create a virtual environment `venv`

   `virtualenv venv`

3. Install the requisite Python libraries using the given `requirements.txt`

   `venv/Scripts/pip install -r requirements.txt`

4. Start the server to access endpoints

   `venv/Scripts/python endpoints.py`