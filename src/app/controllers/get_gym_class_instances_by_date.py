from . import *
import datetime as dt

class GetGymClassInstancesByDate(AppDevController):

  def get_path(self):
    return '/gymclassinstances/date/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    """Takes a string formatted date as input: MM/DD/YYYY
    Example: 03/18/2018 is March 18th, 2018
    """
    date = request.args.get('date')
    input_date = datetime.datetime.strptime(date, '%m/%d/%Y')
    num_days = request.args.get('num_days')

    if num_days is None:
      num_days = 1
    num_days = int(num_days)
    assert num_days >= 1

    gymclass_instances = []
    while (num_days >= 1):
      instances = \
        gymclassinstance_dao.get_gym_class_instances_by_date(input_date)
      gymclass_instances = gymclass_instances + instances
      input_date = input_date + dt.timedelta(1)
      num_days = num_days - 1

    serialized_instances = [
        gymclassinstance_dao.serialize_gym_class_instance(i)
        for i in gymclass_instances
    ]

    return serialized_instances
