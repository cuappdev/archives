from . import *

class Session(Base):
  __tablename__ = 'sessions'

  id = db.Column(db.Integer, primary_key = True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = 'CASCADE'))
  code = db.Column(db.String)
  is_active = db.Column(db.Boolean, default = True)

  def __init__(self, **kwargs):
    self.user_id = kwargs.get('user_id', 0)
    self.code = kwargs.get('code', self.urlsafe_base_64())
    self.is_active = kwargs.get('is_active', False)

  def urlsafe_base_64(self):
    return hashlib.sha1(os.urandom(64)).hexdigest()
