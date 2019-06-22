from tests.test_case import *
from app.dao import gymclass_dao as gcd
from app.dao import instructors_dao as insd
from app.dao import class_descs_dao as cdd

class GymClassesTestCase(TestCase):
  def test_gymclass_methods(self):
    test_ins1 = insd.create_instructor('test_instructor1')[1]
    test_ins2 = insd.create_instructor('test_instructor2')[1]
    test_cd1 = cdd.create_class_desc('test_class_desc1', '')[1]
    test_cd2 = cdd.create_class_desc('test_class_desc2', '')[1]
    test_gymclass = gcd.create_gym_class(test_ins1.id, test_cd1.id)[1]
    test_gymclass2 = gcd.create_gym_class(test_ins2.id, test_cd2.id)[1]
    self.assertEquals(test_gymclass, gcd.get_gym_class_by_id(test_gymclass.id))
    self.assertEquals(test_gymclass2, gcd.get_gym_class_by_id(test_gymclass2.id))
    self.assertIn(test_gymclass, gcd.get_gym_classes_by_instructor(test_ins1.id))
    self.assertIn(test_gymclass2, gcd.get_gym_classes_by_instructor(test_ins2.id))
    self.assertIn(test_gymclass, gcd.get_all_classes())
    self.assertIn(test_gymclass2, gcd.get_all_classes())
