from dao.UserDAO import UserDAO
from log.log import get_logger

logger = get_logger(__name__)
logger.info(f"logger test.")

def testUserDAO():
    newUserId = UserDAO.create_user("testUser01", "123", "user")
    print(newUserId)
    print(UserDAO.get_user_by_username("testUser01"))
    print(UserDAO.update_username(newUserId, "testUser01 - edited"))
    print(UserDAO.delete_user(newUserId))

testUserDAO()