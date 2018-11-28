import os
import requests
from flask import abort, Flask, jsonify, request

app = Flask(__name__)

def is_request_valid(request):
    is_token_valid = request.form['token'] == os.environ['SLACK_VERIFICATION_TOKEN']
    is_team_id_valid = request.form['team_id'] == os.environ['SLACK_TEAM_ID']
    return is_token_valid and is_team_id_valid

@app.route('/', methods=['POST'])
def deploy():
    if not is_request_valid(request):
        return jsonify(
            response_type='in_channel',
            text='This functionality is not available for you.'
        )

    return jsonify(
        response_type='in_channel',
        text='Not implemented yet!'
    )

