import json
from flask import Flask, jsonify, request

app = Flask(__name__)

with open('slack.json') as json_data:
  data = json.load(json_data)

def is_request_valid(request):
  keys = ['channel_id', 'team_id', 'token']
  channel_id, team_id, token = [request.form.get(k, '') for k in keys]
  is_channel_id_valid = channel_id in data['SLACK']['CHANNEL_IDS']
  is_team_id_valid = team_id in data['SLACK']['TEAM_IDS']
  is_token_valid = token == data['SLACK']['TOKEN']
  return all([is_channel_id_valid, is_team_id_valid, is_token_valid])

@app.route('/history/', methods=['POST'])
def history():
  return status('history')

@app.route('/logs/', methods=['POST'])
def logs():
  return status('logs')

@app.route('/uptime/', methods=['POST'])
def uptime():
  return status('uptime')

@app.route('/pem/', methods=['POST'])
def pem():
  if not is_request_valid(request):
    return response('Sorry! /pem is not available for you.')
  text = request.form.get('text', '').lower()
  if not text:
    return response('Please add an app to get /pem for. Ex. /pem eatery')
  if text in data['SLACK']['APPS']:
    if request.form.get('user_id', '') in data['SLACK']['USER_IDS'][text]:
      return response('Getting /pem for {}'.format(text))
    return response('Sorry! /pem {} is not available for you'.format(text))
  return response('Sorry! Could not get /pem for {}. Try one of these: {}'.format(
      text, data['SLACK']['APPS']
  ))

def status(status_type):
  if not is_request_valid(request):
    return response('Sorry! Getting {} is not available for you.'.format(status_type))
  text = request.form.get('text', '').lower()
  if not text:
    return response('Please add an app to get {} for. Ex. /{} eatery'.format(
        status_type, status_type
    ))
  if text in data['SLACK']['APPS']:
    return response('Getting {} for {}...'.format(status_type, text))
  return response('Sorry! Could not get {} for {}. Try one of these: {}'.format(
      status_type, text, data['SLACK']['APPS']
  ))

def response(text):
    return jsonify(
        response_type='in_channel',
        text=text
    )

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)

