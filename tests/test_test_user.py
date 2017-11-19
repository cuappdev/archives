from flask import json
from tests import api_utils
from tests.test_case import *
<<<<<<< HEAD
from tests.test_user import *
from app import constants
from app.pcasts.dao import users_dao, sessions_dao, followings_dao
=======
from app import constants
from app.pcasts.dao import users_dao, sessions_dao, followings_dao
from tests.test_user import *
>>>>>>> Class for TestUser

class TestUserTestCase(TestCase):

  def setUp(self):
<<<<<<< HEAD
    Session.query.delete()
    super(TestUserTestCase, self).setUp()
    Following.query.delete()
    db_session_commit()
=======
    Following.query.delete()
    User.query.delete()
    Session.query.delete()
    db_session_commit()
    super(TestUserTestCase, self).setUp()
    initTestUser()
>>>>>>> Class for TestUser

  def tearDown(self):
    super(TestUserTestCase, self).tearDown()
    Following.query.delete()
<<<<<<< HEAD
    Session.query.delete()
    db_session_commit()

  def test_init_user_goog(self):
    # Create first goog user
    self.assertEquals(self.user1.tokens, {})
    self.assertEquals(self.user1.app_tokens, {})
    self.assertEquals(self.user1.name, '{} {}'.\
        format('default_first_name1', 'default_last_name1'))
    self.assertEquals(self.user1.goog_user_count, 0)
    self.assertEquals(TestUser.goog_user_count, 3)
    self.assertIsNotNone(
        users_dao.get_user_by_id(self.user1.uid, self.user1.uid)
    )
    self.assertIsNotNone(self.user1.session_token)

    # Create second goog user
    self.assertEquals(self.user2.tokens, {})
    self.assertEquals(self.user2.app_tokens, {})
    self.assertEquals(self.user2.name, '{} {}'.\
        format('default_first_name2', 'default_last_name2'))
    self.assertEquals(self.user2.goog_user_count, 1)
    self.assertIsNotNone(
        users_dao.get_user_by_id(self.user2.uid, self.user2.uid)
    )
    self.assertIsNotNone(self.user1.session_token)

  def test_init_user_fb(self):
    fb_app_token = api_utils.get_facebook_app_access_token()

    # First fb user
    fb_user1 = TestUser(
        test_client=self.app,
        name="User one",
        app_access_token=fb_app_token,
        platform=constants.FACEBOOK
    )
    self.assertTrue(fb_user1.tokens != {})
    self.assertTrue(fb_user1.app_tokens != {})
    self.assertEquals(fb_user1.name, "User one")
=======
    User.query.delete()
    Session.query.delete()
    db_session_commit()


  def test_init_user_goog(self):
    # Create first goog user
    g_user1 = TestUser(self.app, name="User one")
    self.assertEquals(g_user1.tokens, {})
    self.assertEquals(g_user1.app_tokens, {})
    self.assertEquals(g_user1.name, "User one")
    self.assertEquals(g_user1.goog_user_count, 0)
    self.assertEquals(TestUser.goog_user_count, 1)
    # After login
    self.assertEquals(constants.NUM_TEST_USERS + 1, \
        users_dao.get_number_users())
    self.assertTrue(users_dao.get_user_by_id(g_user1.uid, g_user1.uid) \
        != None)
    self.assertTrue(g_user1.session_token != None)

    # Create second goog user
    g_user2 = TestUser(self.app, name="User two")
    self.assertEquals(g_user2.tokens, {})
    self.assertEquals(g_user2.app_tokens, {})
    self.assertEquals(g_user2.name, "User two")
    self.assertEquals(g_user2.goog_user_count, 1)
    self.assertEquals(TestUser.goog_user_count, 2)
    # After login
    self.assertEquals(constants.NUM_TEST_USERS + 2, \
        users_dao.get_number_users())
    self.assertTrue(users_dao.get_user_by_id(g_user2.uid, g_user2.uid) != None)
    self.assertTrue(g_user2.session_token != None)

  def test_init_user_fb(self):

    fb_app_token = api_utils.get_facebook_app_access_token()

    # First fb user
    fb_user1 = TestUser(self.app, name="User one", \
        app_access_token=fb_app_token, platform=constants.FACEBOOK)
    self.assertTrue(fb_user1.tokens != {})
    self.assertTrue(fb_user1.app_tokens != {})
    self.assertEquals(fb_user1.name, "User one")
    self.assertEquals(fb_user1.goog_user_count, 0)
    self.assertEquals(TestUser.goog_user_count, 0)
>>>>>>> Class for TestUser
    # After login
    self.assertEquals(constants.NUM_TEST_USERS + 1,\
        users_dao.get_number_users())
    self.assertTrue(users_dao.get_user_by_id(fb_user1.uid, fb_user1.uid)\
        != None)
    self.assertTrue(fb_user1.session_token != None)

    # Second fb user
<<<<<<< HEAD
    fb_user2 = TestUser(
        test_client=self.app,
        name="User two", \
        app_access_token=fb_app_token,
        platform=constants.FACEBOOK
    )
    self.assertTrue(fb_user2.tokens != {})
    self.assertTrue(fb_user2.app_tokens != {})
    self.assertEquals(fb_user2.name, "User two")
=======
    fb_user2 = TestUser(self.app, name="User two", \
        app_access_token=fb_app_token, platform=constants.FACEBOOK)
    self.assertTrue(fb_user2.tokens != {})
    self.assertTrue(fb_user2.app_tokens != {})
    self.assertEquals(fb_user2.name, "User two")
    self.assertEquals(fb_user2.goog_user_count, 0)
    self.assertEquals(TestUser.goog_user_count, 0)
>>>>>>> Class for TestUser
    # After login
    self.assertEquals(constants.NUM_TEST_USERS + 2, \
        users_dao.get_number_users())
    self.assertTrue(users_dao.get_user_by_id(fb_user2.uid, fb_user2.uid) \
        != None)
    self.assertTrue(fb_user2.session_token != None)

  def test_get(self):
    fb_app_token = api_utils.get_facebook_app_access_token()
<<<<<<< HEAD
    fb_user1 = TestUser(
        test_client=self.app, name="User two", \
        app_access_token=fb_app_token,
        platform=constants.FACEBOOK
    )

    response = fb_user1.get("api/v1/users/me/")
    response = json.loads(response.data)
    self.assertEquals(response['data']['user']['id'], fb_user1.uid)
    response = self.user1.get("api/v1/users/me/")
    response = json.loads(response.data)
    self.assertEquals(response['data']['user']['id'], self.user1.uid)

  def test_post(self):
    fb_app_token = api_utils.get_facebook_app_access_token()
    fb_user1 = TestUser(
        test_client=self.app,
        name="User two",
        app_access_token=fb_app_token,
        platform=constants.FACEBOOK
    )

    response = fb_user1.post("api/v1/followings/{}/".format(self.user1.uid))
    response = json.loads(response.data)
    self.assertIsNotNone(response['data']['following'])
    response = self.user1.post("api/v1/followings/{}/".format(fb_user1.uid))
    response = json.loads(response.data)
    self.assertIsNotNone(response['data']['following'])

  def test_delete(self):
    fb_app_token = api_utils.get_facebook_app_access_token()
    fb_user1 = TestUser(
        test_client=self.app,
        name="User two",
        app_access_token=fb_app_token,
        platform=constants.FACEBOOK
    )

    followings_dao.create_following(self.user1.uid, fb_user1.uid)
    followings_dao.create_following(fb_user1.uid, self.user1.uid)
    response = fb_user1.delete("api/v1/followings/{}/".format(self.user1.uid))
    response = json.loads(response.data)
    self.assertEquals(response['data'], {})
    response = self.user1.delete("api/v1/followings/{}/".format(fb_user1.uid))
    response = json.loads(response.data)
    self.assertEquals(response['data'], {})
=======
    g_user1 = TestUser(self.app, name="User one")
    fb_user1 = TestUser(self.app, name="User two", \
        app_access_token=fb_app_token, platform=constants.FACEBOOK)

    response = fb_user1.get("api/v1/users/me/")
    self.assertEquals(response['user']['id'], fb_user1.uid)
    response = g_user1.get("api/v1/users/me/")
    self.assertEquals(response['user']['id'], g_user1.uid)


  def test_post(self):
    fb_app_token = api_utils.get_facebook_app_access_token()
    g_user1 = TestUser(self.app, name="User one")
    fb_user1 = TestUser(self.app, name="User two", \
        app_access_token=fb_app_token, platform=constants.FACEBOOK)

    response = fb_user1.post("api/v1/followings/{}/".format(g_user1.uid))
    self.assertTrue(response['following'] != None)
    response = g_user1.post("api/v1/followings/{}/".format(fb_user1.uid))
    self.assertTrue(response['following'] != None)

  def test_delete(self):
    fb_app_token = api_utils.get_facebook_app_access_token()
    g_user1 = TestUser(self.app, name="User one")
    fb_user1 = TestUser(self.app, name="User two", \
        app_access_token=fb_app_token, platform=constants.FACEBOOK)

    followings_dao.create_following(g_user1.uid, fb_user1.uid)
    followings_dao.create_following(fb_user1.uid, g_user1.uid)
    response = fb_user1.delete("api/v1/followings/{}/".format(g_user1.uid))
    self.assertEquals(response, {})
    response = g_user1.delete("api/v1/followings/{}/".format(fb_user1.uid))
    self.assertEquals(response, {})
>>>>>>> Class for TestUser
