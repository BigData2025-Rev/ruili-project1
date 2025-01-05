import unittest
from dao.UserDAO import UserDAO
from log.log import get_logger

class TestUserDAO(unittest.TestCase):
    def setUp(self):
        # create a user before each test
        self.logger = get_logger(__name__)
        self.logger.info("Setting up test environment...")
        self.test_username = "testUser01"
        self.test_password = "123"
        self.test_role = "user"
        self.new_user_id = UserDAO.create_user(self.test_username, self.test_password, self.test_role)

    def tearDown(self):
        # make sure to delete the user after test
        self.logger.info("Tearing down test environment...")
        if self.new_user_id:
            UserDAO.delete_user(self.new_user_id)

    def test_create_user(self):
        # check create a user
        self.assertIsNotNone(self.new_user_id, "Failed to create user")
        user = UserDAO.get_user_by_username(self.test_username)
        self.assertIsNotNone(user, "User should exist after creation")
        self.assertEqual(user.username, self.test_username)

    def test_update_username(self):
        # check update username
        updated = UserDAO.update_username(self.new_user_id, "testUser01_edited")
        self.assertEqual(updated, 1, "Failed to update username")
        updated_user = UserDAO.get_user_by_username("testUser01_edited")
        self.assertIsNotNone(updated_user, "Updated username should exist in the database")
        self.assertEqual(updated_user.username, "testUser01_edited")

    def test_delete_user(self):
        # checl delete user
        deleted = UserDAO.delete_user(self.new_user_id)
        self.assertEqual(deleted, 1, "Failed to delete user")
        deleted_user = UserDAO.get_user_by_username(self.test_username)
        self.assertIsNone(deleted_user, "User should not exist after deletion")

if __name__ == '__main__':
    unittest.main()
