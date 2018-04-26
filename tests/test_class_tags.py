from tests.test_case import *
from app.dao import class_tags_dao as ctd
from app.dao import class_descs_dao as cdd

class ClassTagsTestCase(TestCase):
  def test_class_tags_methods(self):
    test_tag = ctd.create_class_tag("test1")[1]
    self.assertIn(test_tag, ctd.get_all_tags())
    self.assertEqual(test_tag, ctd.get_class_tag_by_name("test1"))
    self.assertEqual(test_tag, ctd.get_class_tag_by_id(test_tag.id))
