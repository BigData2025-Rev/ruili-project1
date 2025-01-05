from flask import render_template, jsonify, request, redirect, url_for
from app import app  # 从 app.py 导入 app 实例
from service.UserService import UserService

@app.route('/')
def index():
    print("Get index request.")
    return render_template('index.html')

@app.route('/welcome')
def welcome():
    print("Get welcome request.")
    return render_template('welcome.html')

@app.route('/register', methods=['POST'])
def register():
    print("Get register request.")
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"success": False, "message": "Invalid input."}), 400

    result = UserService.register_user(data['username'], data['password'])
    return jsonify(result)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"success": False, "message": "Invalid input."}), 400

    result = UserService.login_user(data['username'], data['password'])
    return jsonify(result)

@app.route('/logout', methods=['GET'])
def logout():
    print("Get logout request.")
    return jsonify({"success": True, "message": "Logged out successfully."})
