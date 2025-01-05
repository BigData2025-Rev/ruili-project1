from dao.UserDAO import UserDAO
from log.log import get_logger

print(UserDAO.get_user_by_username("admin"))
logger = get_logger(__name__)
logger.info(f"logger test.")