import base64
import six

def make_authorization_headers(client_id, client_secret):
  auth_header = \
    base64.\
    b64encode(six.text_type(client_id + ':' + client_secret).encode('ascii'))
  return {'Authorization': 'Basic %s' % auth_header.decode('ascii')}
