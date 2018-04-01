import datetime as dt
from flask import json
from tests.test_case import *
from app.dao import gymclassinstance_dao as gcid
from app.dao import gymclass_dao as gcd
from app.dao import instructors_dao as insd
from app.dao import class_descs_dao as cdd

class GymClassInstancesTestCase(TestCase):
  def test_gymclassinstance_methods(self):
    test_args = {
        "class_name": "test_class",
        "date": "01/01/1900",
        "location": "test_loc",
        "instructor_name": "test_instructor1",
        "is_cancelled": False,
        "start_time": "3:00PM",
        "end_time": "4:00PM",
    }
    test_args2 = {
        "class_name": "test_class2",
        "date": "01/01/1900",
        "location": "test_loc2",
        "instructor_name": "test_instructor2",
        "is_cancelled": True,
        "start_time": "4:00PM",
        "end_time": "5:00PM",
    }
    test_cd = cdd.create_class_desc('test_class', 'test_class_desc')[1]
    test_cd2 = cdd.create_class_desc('test_class2', 'test_class_desc2')[1]
    test_gymclassinstance = gcid.create_gym_class_instance(test_args)[1]
    test_gymclassinstance2 = gcid.create_gym_class_instance(test_args2)[1]
    self.assertEquals(test_gymclassinstance,
        gcid.get_gym_class_instance_by_id(test_gymclassinstance.id))
    self.assertEquals(test_gymclassinstance2,
        gcid.get_gym_class_instance_by_id(test_gymclassinstance2.id))
    self.assertIn(test_gymclassinstance, gcid.get_all_gym_class_instances(None))
    self.assertIn(test_gymclassinstance2,
        gcid.get_all_gym_class_instances(None))
    self.assertIn(test_gymclassinstance,
        gcid.get_gym_class_by_start_duration(test_gymclassinstance.gym_class_id,
        test_gymclassinstance.gym_id, test_gymclassinstance.start_dt,
        test_gymclassinstance.duration))
    self.assertIn(test_gymclassinstance,
        gcid.get_all_classes_by_start_duration(test_gymclassinstance.start_dt,
        test_gymclassinstance.duration))
    self.assertNotIn(test_gymclassinstance2,
        gcid.get_all_classes_by_start_duration(test_gymclassinstance.start_dt,
        test_gymclassinstance.duration))
    self.assertIn(test_gymclassinstance,
        gcid.get_gym_class_instances_not_cancelled())
    self.assertNotIn(test_gymclassinstance2,
        gcid.get_gym_class_instances_not_cancelled())
    self.assertIn(test_gymclassinstance,
        gcid.get_gym_class_instances_by_time(datetime.datetime.strptime("3:01PM",
        '%I:%M%p')))
    self.assertNotIn(test_gymclassinstance,
        gcid.get_gym_class_instances_by_time(datetime.datetime.strptime("2:01PM",
        '%I:%M%p')))
    self.assertNotIn(test_gymclassinstance2,
        gcid.get_gym_class_instances_by_time(datetime.datetime.strptime("3:01PM",
        '%I:%M%p')))
    self.assertIn(test_gymclassinstance2,
        gcid.get_gym_class_instances_by_time(datetime.datetime.strptime("4:01PM",
        '%I:%M%p')))
