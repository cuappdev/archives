from flask import Flask, render_template, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from constants import *
import os

# Configure Flask app
app = Flask(__name__, static_url_path = '/static')
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Database
db = SQLAlchemy(app)

# Import + Register Blueprints
from app.tempo import tempo as tempo
app.register_blueprint(tempo)

# HTTP error handling
@app.errorhandler(404)
def not_found(error):
  return render_template('404.html'), 404
