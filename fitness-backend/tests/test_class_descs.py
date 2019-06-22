from tests.test_case import *
from app.dao import class_descs_dao as cdd

class ClassDescsTestCase(TestCase):
  def test_classdescs_methods(self):
    test_cdd1 = cdd.create_class_desc('test_name', 'test_desc')[1]
    test_cdd2 = cdd.create_class_desc('test_name2', 'test_desc2')[1]
    self.assertEquals(test_cdd1, cdd.get_class_desc_by_name('test_name'))
    self.assertEquals(test_cdd2, cdd.get_class_desc_by_name('test_name2'))
    self.assertEquals(test_cdd1, cdd.get_class_desc_by_id(test_cdd1.id))
    self.assertEquals(test_cdd2, cdd.get_class_desc_by_id(test_cdd2.id))
    self.assertIn(test_cdd1, cdd.get_all_class_descs())
    self.assertIn(test_cdd2, cdd.get_all_class_descs())
