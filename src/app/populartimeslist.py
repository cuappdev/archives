from . import *

class PopularTimesList(Base):
  __tablename__ = 'popular_times_list'

  id = db.Column(db.Integer, primary_key=True)
  monday = db.Column(db.String(255))
  tuesday = db.Column(db.String(255))
  wednesday = db.Column(db.String(255))
  thursday = db.Column(db.String(255))
  friday = db.Column(db.String(255))
  saturday = db.Column(db.String(255))
  sunday = db.Column(db.String(255))

  gym_id = db.Column(
      db.Integer,
      db.ForeignKey('gym.id', ondelete='CASCADE')
  )
  class_desc = db.relationship('Gym', backref='populartimeslist')

  def __init__(self, **kwargs):
    self.monday = kwargs.get('monday')
    self.tuesday = kwargs.get('tuesday')
    self.wednesday = kwargs.get('wednesday')
    self.thursday = kwargs.get('thursday')
    self.friday = kwargs.get('friday')
    self.saturday = kwargs.get('saturday')
    self.sunday = kwargs.get('sunday')

    self.gym_id = kwargs.get('gym_id')
