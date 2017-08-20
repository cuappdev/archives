from . import *

class Notification(Base):
  __tablename__ = 'notifications'

  id = db.Column(db.Integer, primary_key = True)
  from_id = db.Column(db.Integer, nullable = False, name = 'from')
  to_id = db.Column(db.Integer, nullable = False, name = 'to')
  notification_type = db.Column(db.Integer, nullable = False)
  seen = db.Column(db.Boolean)
  post_id = db.Column(db.Integer)
  message = db.Column(db.String)

  def __init__(self, **kwargs):
    self.from_id = kwargs.get('from_id', 0)
    self.to_id = kwargs.get('to_id', 0)
    self.notification_type = kwargs.get('notification_type', 0)
    self.seen = kwargs.get('seen', False)
    self.post_id = kwargs.get('post_id', 0)
    self.message = kwargs.get('message', '')
