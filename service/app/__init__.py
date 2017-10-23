import os
from flask import Flask, render_template, jsonify, make_response

# Configure Flask app
app = Flask(__name__, static_url_path='/templates')

# Import + Register Blueprints
from app.podcastml import podcastml as podcastml # pylint: disable=C0413
app.register_blueprint(podcastml)

# HTTP error handling
@app.errorhandler(404)
def not_found(error):
  return render_template('404.html'), 404
