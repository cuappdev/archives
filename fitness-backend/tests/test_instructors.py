from tests.test_case import *
from app.dao import instructors_dao as insd

class InstructorsTestCase(TestCase):
  def test_instructor_methods(self):
    test_inst = insd.create_instructor("test1")[1]
    self.assertEquals(test_inst.id, insd.get_instructor_by_name("test1").id)
    self.assertEquals("test1", insd.get_instructor_by_id(test_inst.id).name)
    # test for get_all
    test_inst2 = insd.create_instructor("test2")[1]
    all_inst = insd.get_all_instructors()
    self.assertIn(test_inst, all_inst)
    self.assertIn(test_inst2, all_inst)
