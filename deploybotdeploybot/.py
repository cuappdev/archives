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

@app.route('/deploy/', methods=['POST'])
def deploy():
  if not is_request_valid(request):
    return response('Sorry! Deploying is not available for you.')
  text = request.form.get('text', '').lower()
  if not text:
    return response('Please add an app to deploy. Ex: /deploy eatery')
  if text in data['SLACK']['APPS']:
    if request.form['user_id'] in data['SLACK']['USER_IDS'][text]:
      return response('Deploying {}...'.format(text))
    return response('Sorry! Deploying {} is not available for you.'.format(text))
  return response(
      'Sorry! Could not deploy {}. Try one of these: {}'.format(
           text, ', '.join([a for a in data['SLACK']['APPS']])
      )
  )

@app.route('/stat/', methods=['POST'])
def status():
  if not is_request_valid(request):
    return response('Sorry! Getting a status is not available for you.')
  text = request.form.get('text', '').lower().split()
  if not text or len(text) != 2:
    return response('Please add an app and status type. Ex: /stat transit uptime')
  if text[0] in data['SLACK']['APPS'] and text[1] in data['SLACK']['STATUS_TYPES']:
    return response('Getting {} for {}...'.format(text[1], text[0]))
  if text[0] not in data['SLACK']['APPS']:
    return response(
        'Sorry! Could not get a status for {}. Try one of these: {}'.format(
            text[0], ', '.join([a for a in data['SLACK']['APPS']])
        )
    )
  if text[1] not in data['SLACK']['STATUS_TYPES']:
    return response(
        'Sorry! Could not get {} for {}. Try getting a status of type: {}'.format(
            text[1], text[0], ', '.join([s for s in data['SLACK']['STATUS_TYPES']])
        )
    )
  return response(
      'Sorry! Could not get status. Try one of these: {}'.format(
          text, ', '.join([s for s in data['SLACK']['STATUS_TYPES']])
      )
  )

def response(text):
    return jsonify(
        response_type='in_channel',
        text=text
    )

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)

