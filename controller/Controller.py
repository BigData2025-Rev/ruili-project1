# controller/Controller.py
from flask import Flask, request, jsonify
from service.UserService import UserService

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    result = UserService.register_user(data['username'], data['password'])
    return jsonify(result)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    result = UserService.login_user(data['username'], data['password'])
    return jsonify(result)
