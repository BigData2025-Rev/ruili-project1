from flask import render_template, jsonify, request, redirect, url_for, session
from app import app  # 从 app.py 导入 app 实例
from service.UserService import UserService

@app.route('/')
def index():
    # 检查用户是否已登录
    if 'user_id' in session:
        return redirect(url_for('welcome'))  # 已登录，重定向到欢迎页面
    # 未登录，渲染主页
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    # 接收注册请求
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"success": False, "message": "Invalid input."}), 400

    # 调用 UserService 进行注册
    result = UserService.register_user(data['username'], data['password'])
    return jsonify(result)

@app.route('/login', methods=['POST'])
def login():
    # 接收登录请求
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"success": False, "message": "Invalid input."}), 400

    # 调用 UserService 验证用户
    result = UserService.login_user(data['username'], data['password'])
    if result['success']:
        # 登录成功，将用户信息存入 Session
        session['user_id'] = result['token']  # 存储 JWT 令牌
        session['username'] = data['username']
        return redirect(url_for('welcome'))  # 跳转到欢迎页面
    return jsonify(result)

@app.route('/welcome')
def welcome():
    # 检查用户是否已登录
    if 'user_id' not in session:
        return redirect(url_for('index'))  # 如果未登录，重定向到登录页面
    return render_template('welcome.html', username=session.get('username'))

@app.route('/logout', methods=['GET'])
def logout():
    # 清除 Session 数据
    session.clear()
    return jsonify({"success": True, "message": "Logged out successfully."})
