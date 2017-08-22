from . import *
import datetime

class User(Base):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String)
  hipster_score = db.Column(db.Integer, default = 0)
  caption = db.Column(db.String)
  followers_count = db.Column(db.Integer, default = 0)
  location_id = db.Column(db.Integer) # TODO - remove this
  like_count = db.Column(db.Integer, default = 0)
  fbid = db.Column(db.String, unique = True)
  username = db.Column(db.String(256, collation='NOCASE'), unique = True)
  email = db.Column(db.String)
  followings_count = db.Column(db.Integer, default = 0)
  push_id = db.Column(db.String)
  remote_push_notifications_enabled = db.column(db.Boolean)
  last_active = db.Column(db.DateTime, default = db.func.current_timestamp())

  def __init__(self, **kwargs):
    self.name = kwargs.get('name', '')
    self.hipster_score = kwargs.get('hipster_score', 0)
    self.caption = kwargs.get('caption', '')
    self.followers_count = kwargs.get('followers_count', 0)
    self.location_id = kwargs.get('location_id', 0)
    self.like_count = kwargs.get('like_count', 0)
    self.fbid = kwargs.get('fbid', 0)
    self.username = kwargs.get('username', 'temp_username_{}'.format(self.fbid))
    self.email = kwargs.get('email', '')
    self.followings_count = kwargs.get('followings_count', 0)
    self.push_id = kwargs.get('push_id', '')
    self.remote_push_notifications_enabled = kwargs.get('remote_push_notifications_enabled', False)
    self.last_active = kwargs.get('', datetime.datetime.now())
