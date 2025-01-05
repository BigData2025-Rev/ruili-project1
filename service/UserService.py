import bcrypt
import jwt
from dao.UserDAO import UserDAO
from datetime import datetime, timedelta, timezone
from config.config import Config

SECRET_KEY = Config.UserServiceSecretKey  # Import secret key from config


class UserService:
    @staticmethod
    def register_user(username, password, role="user"):
        # Check if username and password valid
        existing_user = UserDAO.get_user_by_username(username)
        if existing_user:
            return {"success": False, "message": "Username already exists."}
        if not str(username).isalnum():
            return {"success": False, "message": "Username can only include alpha and numbers."}
        if len(username) < 1 or len(username) > 10:
            return {"success": False, "message": "Username length must be in 1 to 10."}
        if len(password) < 6 or len(password) > 20:
            return {"success": False, "message": "Password length must be in 6 to 20."}
        
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Create user in the database
        user_id = UserDAO.create_user(username, hashed_password.decode('utf-8'), role)
        if user_id:
            return {"success": True, "message": "User registered successfully.", "user_id": user_id}
        return {"success": False, "message": "Failed to register user."}

    @staticmethod
    def login_user(username, password):
        user = UserDAO.get_user_by_username(username)
        if not user:
            return {"success": False, "message": "Invalid username or password."}

        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return {"success": False, "message": "Invalid username or password."}

        # Generate JWT token
        payload = {
            "user_id": user.id,
            "username": user.username,
            "role": user.role,
            "exp": datetime.now(timezone.utc) + timedelta(hours=2)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return {"success": True, "message": "Login successful.", "token": token, "payload": payload}

    @staticmethod
    def get_all_users():
        users = UserDAO.get_all_users()
        # Filter sensitive information
        filtered_users = [{"user_id": user.id, "username": user.username, "role": user.role} for user in users]
        return {"success": True, "users": filtered_users}

    @staticmethod
    def delete_user_by_id(user_id):
        user = UserDAO.get_user_by_id(user_id)
        if not user:
            return {"success": False, "message": "User not found."}
        if user.role == 'admin':
            return {"success": False, "message": "Cannot delete admin users."}

        affected_rows = UserDAO.delete_user_by_id(user_id)
        if affected_rows > 0:
            return {"success": True, "message": "User deleted successfully."}
        return {"success": False, "message": "Failed to delete user."}

    @staticmethod
    def update_user_role_by_user_id(user_id, role):
        user = UserDAO.get_user_by_id(user_id)
        if not user:
            return {"success": False, "message": "User not found."}
        if user.role == 'admin' and role != 'admin':
            return {"success": False, "message": "Cannot change role of admin users."}

        affected_rows = UserDAO.update_role_by_id(user_id, role)
        if affected_rows > 0:
            return {"success": True, "message": f"User role updated to {role}."}
        return {"success": False, "message": "Failed to update user role."}