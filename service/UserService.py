# service/UserService.py

import bcrypt
import jwt
from dao.UserDAO import UserDAO
from datetime import datetime, timedelta, timezone
from config.config import Config

SECRET_KEY = Config.UserServiceSecretKey

class UserService:
    @staticmethod
    def register_user(username, password, role="user"):

        print("Get register request: " + username + " " + password)

        # 检查用户名是否已存在
        existing_user = UserDAO.get_user_by_username(username)
        if existing_user:
            return {"success": False, "message": "Username already exists."}

        # 验证密码强度
        if len(password) < 6:
            return {"success": False, "message": "Password too short (minimum 6 characters)."}

        # 加密密码
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # 创建用户
        user_id = UserDAO.create_user(username, hashed_password.decode('utf-8'), role)
        if user_id:
            return {"success": True, "message": "User registered successfully.", "user_id": user_id}
        else:
            return {"success": False, "message": "Failed to register user."}
    
    @staticmethod
    def login_user(username, password):
        user = UserDAO.get_user_by_username(username)
        if not user:
            return {"success": False, "message": "Invalid username or password."}

        # 验证密码
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return {"success": False, "message": "Invalid username or password."}

        # 生成 JWT 令牌
        payload = {
            "user_id": user.id,
            "username": user.username,
            "role": user.role,
            "exp": datetime.now(timezone.utc) + timedelta(hours=2)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return {"success": True, "message": "Login successful.", "token": token}