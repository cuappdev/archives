from flask import request, jsonify
from functools import wraps # for decorators
import abc

# A REST-API controller that handles boilerplate for
# serving up JSON responses based on HTTP verbs
class AppDevController:
  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def get_path(self): # URI-path that begins and ends with a '/'
    return ''

  @abc.abstractmethod
  def get_methods(self): # List of different HTTP methods supported
    return []

  @abc.abstractmethod
  def content(self, **kwargs):
    return dict()

  def get_name(self):
    return self.get_path().replace('/', '-')

  def response(self):
    try:
      content = self.content()
      return jsonify({
        'success': True,
        'data': content
      })
    except Exception as e:
      print e
      return jsonify({
        'success': False,
        'data': { 'errors': [str(e)] }
      })
