from . import *

class PopularTimesList(Base):
  """ Class representing popular times data from Google

  Sample Data for Helen Newman on Monday:
  [15,25,27,22,21,31,47,53,45,34,36,52,70,75,60,35,14,0]

  Each number represents the popularity at that hour on a scale from 0-100
  Data is only available for hours that the gym is open for
  """
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
      db.ForeignKey('gyms.id', ondelete='CASCADE')
  )
  gym = db.relationship('Gym', backref='popular_times_list')

  def __init__(self, **kwargs):
    self.monday = kwargs.get('monday')
    self.tuesday = kwargs.get('tuesday')
    self.wednesday = kwargs.get('wednesday')
    self.thursday = kwargs.get('thursday')
    self.friday = kwargs.get('friday')
    self.saturday = kwargs.get('saturday')
    self.sunday = kwargs.get('sunday')

    self.gym_id = kwargs.get('gym_id')
