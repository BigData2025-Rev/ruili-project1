import bcrypt
import jwt
from dao.UserDAO import UserDAO
from datetime import datetime, timedelta, timezone
from config.config import Config
from log.log import get_logger

logger = get_logger(__name__)

SECRET_KEY = Config.UserServiceSecretKey  # Import secret key from config


class UserService:

    @staticmethod
    def register_user(username, password, role="user"):
        logger.info(f"Attempting to register user: username={username}, role={role}")
        
        # Validate username and password
        if UserDAO.get_user_by_username(username):
            logger.warning(f"Registration failed: Username already exists. username={username}")
            return {"success": False, "message": "Username already exists."}
        if not username.isalnum():
            logger.warning("Registration failed: Username contains invalid characters.")
            return {"success": False, "message": "Username can only include alpha and numbers."}
        if not (1 <= len(username) <= 10):
            logger.warning("Registration failed: Username length out of bounds.")
            return {"success": False, "message": "Username length must be in 1 to 10."}
        if not (6 <= len(password) <= 20):
            logger.warning("Registration failed: Password length out of bounds.")
            return {"success": False, "message": "Password length must be in 6 to 20."}
        
        # Hash the password and create user
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_id = UserDAO.create_user(username, hashed_password.decode('utf-8'), role)
        if user_id:
            logger.info(f"User registered successfully: username={username}, user_id={user_id}")
            return {"success": True, "message": "User registered successfully.", "user_id": user_id}
        logger.error(f"Failed to register user: username={username}")
        return {"success": False, "message": "Failed to register user."}

    @staticmethod
    def login_user(username, password):
        logger.info(f"Attempting to login user: username={username}")
        user = UserDAO.get_user_by_username(username)
        if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            logger.warning(f"Login failed: Invalid username or password. username={username}")
            return {"success": False, "message": "Invalid username or password."}

        # Generate JWT token
        payload = {
            "user_id": user.id,
            "username": user.username,
            "role": user.role,
            "exp": datetime.now(timezone.utc) + timedelta(hours=2)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        logger.info(f"User logged in successfully: username={username}, user_id={user.id}")
        return {"success": True, "message": "Login successful.", "token": token, "payload": payload}

    @staticmethod
    def get_all_users():
        logger.info("Fetching all users.")
        users = UserDAO.get_all_users()
        filtered_users = [{"user_id": user.id, "username": user.username, "role": user.role, "deposit": user.deposit} for user in users]
        logger.info(f"Fetched {len(users)} users.")
        return {"success": True, "users": filtered_users}

    @staticmethod
    def get_current_deposit_by_id(user_id):
        logger.info(f"Fetching deposit for user_id={user_id}.")
        user = UserDAO.get_user_by_id(user_id)
        if not user:
            logger.warning(f"User not found: user_id={user_id}")
            return {"success": False, "deposit": 0.00, "message": f"User with id {user_id} does not exist."}
        return {"success": True, "deposit": float(user.deposit)}

    @staticmethod
    def add_money_to_deposit_by_id(user_id, amount):
        logger.info(f"Adding money to deposit: user_id={user_id}, amount={amount}")
        if amount <= 0:
            logger.warning("Invalid deposit amount: Amount must be positive.")
            return {"success": False, "message": "Amount must be positive."}

        user = UserDAO.get_user_by_id(user_id)
        if not user:
            logger.warning(f"User not found: user_id={user_id}")
            return {"success": False, "message": f"User with id {user_id} does not exist."}

        new_deposit = user.deposit + amount
        if UserDAO.update_user_deposit_by_id(user_id, new_deposit) > 0:
            logger.info(f"Deposit updated successfully: user_id={user_id}, new_deposit={new_deposit}")
            return {"success": True, "message": f"Deposit updated successfully. New deposit: {new_deposit}"}
        logger.error(f"Failed to update deposit: user_id={user_id}")
        return {"success": False, "message": "Failed to update deposit."}

    @staticmethod
    def minus_money_to_deposit_by_id(user_id, amount):
        logger.info(f"Deducting money from deposit: user_id={user_id}, amount={amount}")
        if amount <= 0:
            logger.warning("Invalid deduction amount: Amount must be positive.")
            return {"success": False, "message": "Amount must be positive."}

        user = UserDAO.get_user_by_id(user_id)
        if not user:
            logger.warning(f"User not found: user_id={user_id}")
            return {"success": False, "message": f"User with id {user_id} does not exist."}

        if user.deposit < amount:
            logger.warning(f"Insufficient deposit: user_id={user_id}, current_deposit={user.deposit}, requested_deduction={amount}")
            return {"success": False, "message": "Insufficient deposit."}

        new_deposit = user.deposit - amount
        if UserDAO.update_user_deposit_by_id(user_id, new_deposit) > 0:
            logger.info(f"Deposit deducted successfully: user_id={user_id}, new_deposit={new_deposit}")
            return {"success": True, "message": f"Deposit updated successfully. New deposit: {new_deposit}"}
        logger.error(f"Failed to deduct deposit: user_id={user_id}")
        return {"success": False, "message": "Failed to update deposit."}

    @staticmethod
    def delete_user_by_id(user_id):
        logger.info(f"Attempting to delete user: user_id={user_id}")
        user = UserDAO.get_user_by_id(user_id)
        if not user:
            logger.warning(f"User not found: user_id={user_id}")
            return {"success": False, "message": "User not found."}
        if user.role == 'admin':
            logger.warning(f"Cannot delete admin user: user_id={user_id}")
            return {"success": False, "message": "Cannot delete admin users."}

        if UserDAO.delete_user_by_id(user_id) > 0:
            logger.info(f"User deleted successfully: user_id={user_id}")
            return {"success": True, "message": "User deleted successfully."}
        logger.error(f"Failed to delete user: user_id={user_id}")
        return {"success": False, "message": "Failed to delete user."}

    @staticmethod
    def update_user_role_by_user_id(user_id, role):
        logger.info(f"Updating user role: user_id={user_id}, new_role={role}")
        user = UserDAO.get_user_by_id(user_id)
        if not user:
            logger.warning(f"User not found: user_id={user_id}")
            return {"success": False, "message": "User not found."}
        if user.role == 'admin' and role != 'admin':
            logger.warning(f"Cannot change role of admin user: user_id={user_id}")
            return {"success": False, "message": "Cannot change role of admin users."}

        if UserDAO.update_role_by_id(user_id, role) > 0:
            logger.info(f"User role updated successfully: user_id={user_id}, new_role={role}")
            return {"success": True, "message": f"User role updated to {role}."}
        logger.error(f"Failed to update user role: user_id={user_id}")
        return {"success": False, "message": "Failed to update user role."}
