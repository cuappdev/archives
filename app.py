import datetime
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify

app = Flask(__name__)

current_uid = None

app.config.from_object('config');

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'log_db'):
        g.log_db = connect_db()
    return g.log_db

@app.before_first_request
def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('log_schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print 'Initialized the database.'

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'log_db'):
        g.log_db.close()

@app.route('/')
def hello_world():
    return 'Big Red Shuttle - Logging Endpoints'

@app.route('/register', methods=['POST'])
def register():
    global current_uid
    uid = request.json['uid']
    key = request.json['key']
    if key in app.config['KEYS']:
        current_uid = uid
        return jsonify(result="success")
    return jsonify(result="Invalid key")

@app.route('/log', methods=['POST'])
def log():
    global current_uid
    db = get_db()
    uid = request.json['uid']
    if uid != current_uid:
        return jsonify(result="Unregistered uid")
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    date = datetime.datetime.now()
    db.execute('insert into entries (uid, latitude, longitude, date) values (?, ?, ?, ?)', [uid, latitude, longitude, date])
    db.commit()
    return jsonify(result="success")

def dict_from_row(row):
    return dict(zip(row.keys(), row))

@app.route('/latest', methods=['GET'])
def latest():
    db = get_db()
    uid = request.args['uid']
    cur = db.execute('select * from entries where uid = ? order by date desc limit 1', [uid])
    entry = cur.fetchone()
    if entry == None:
        return jsonify(result="no log available")
    row = dict_from_row(entry);
    row['result']='success'
    return jsonify(row)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6001)
