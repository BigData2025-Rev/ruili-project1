from flask import render_template, jsonify, request, redirect, url_for, session
from app import app
from service.UserService import UserService
from service.ProductService import ProductService
from service.OrderService import OrderService

@app.route('/')
def index():
    # Redirect to welcome page if user is already logged in
    if 'token' in session:
        return redirect(url_for('welcome'))
    return render_template('index.html')  # Render home page for unauthenticated users

@app.route('/register', methods=['POST'])
def register():
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
    if result['success']:
        session['token'] = result['token']  # Store JWT token in session
        session['user_id'] = result['payload']['user_id']
        session['username'] = result['payload']['username']  # Store username in session
        session['role'] = result['payload']['role']
        session['exp'] = result['payload']['exp']
        return redirect(url_for('welcome'))  # Redirect to welcome page on success
    return jsonify(result)

@app.route('/welcome')
def welcome():
    # Redirect to home page if user is not logged in
    if 'token' not in session:
        return redirect(url_for('index'))
    return render_template('welcome.html', username=session.get('username'))


"""
User Related API
"""

@app.route('/admin', methods=['GET'])
def admin_page():
    if 'token' not in session:
        return jsonify({"success": False, "message": "Unauthorized access."}), 401
    if session['role'] != 'admin':
        return jsonify({"success": False, "message": "You are not admin user. You cannot access this page."}), 403
    return render_template('admin.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()  # Clear all session data
    return jsonify({"success": True, "message": "Logged out successfully."})

@app.route('/users', methods=['GET'])
def get_all_users():
    if 'token' not in session:
        return jsonify({"success": False, "message": "Unauthorized access."}), 401
    if session['role'] != 'admin':
        return jsonify({"success": False, "message": "Only admin users can perform this action."}), 403

    result = UserService.get_all_users()
    return jsonify(result)

@app.route('/user', methods=['DELETE'])
def delete_user_by_id():
    if 'token' not in session:
        return jsonify({"success": False, "message": "Unauthorized access."}), 401
    if session['role'] != 'admin':
        return jsonify({"success": False, "message": "Only admin users can perform this action."}), 403

    data = request.json
    if not data or 'user_id' not in data:
        return jsonify({"success": False, "message": "User ID is required."}), 400

    result = UserService.delete_user_by_id(data['user_id'])
    return jsonify(result)

@app.route('/user/role', methods=['PUT'])
def update_role_by_id():
    if 'token' not in session:
        return jsonify({"success": False, "message": "Unauthorized access."}), 401
    if session['role'] != 'admin':
        return jsonify({"success": False, "message": "Only admin users can perform this action."}), 403

    data = request.json
    if not data or 'user_id' not in data or 'role' not in data:
        return jsonify({"success": False, "message": "User ID and new role are required."}), 400

    result = UserService.update_user_role_by_user_id(data['user_id'], data['role'])
    return jsonify(result)


"""
Product related API
"""

@app.route('/products', methods=['GET'])
def get_all_products():
    if 'token' not in session:
        return redirect(url_for('index'))
    products = ProductService.get_all_products()
    return jsonify(products), 200

@app.route('/product', methods=['PUT'])
def add_product():
    # add a new product
    # the request.json should include:
    #   product name
    #   product price
    #   product inventory
    #   product category (can be empty)
    #   product description (can be empty) 
    if 'token' not in session:
        return redirect(url_for('index'))
    if session['role'] != 'admin':
        return jsonify({"success": False, "message": "Only admin users can perform this action."}), 403
    data = request.json
    if not data or 'name' not in data or 'price' not in data or 'inventory' not in data \
        or "category" not in data or "description" not in data:
        return jsonify({"success": False, "message": "Invalid input."}), 400
    result = ProductService.add_product(data)
    return jsonify(result), (201 if result["success"] else 500)

@app.route('/product/inventory', methods=['PUT'])
def update_product_inventory():
    if 'token' not in session:
        return redirect(url_for('index'))
    # update product inventory
    # the request.json should include product_id, product_change_amount(int, + or -)
    data = request.json
    if not data or 'product_id' not in data or 'change_amount' not in data:
        return jsonify({"success": False, "message": "Invalid input."}), 400
    result = ProductService.update_inventory_by_id(data['product_id'], data['change_amount'])
    return jsonify(result), (200 if result["success"] else 500)

@app.route('/product/price', methods=['PUT'])
def update_product_price():
    # update product price
    # the request.json should include product_id, product_new_price(int)
    if 'token' not in session:
        return redirect(url_for('index'))
    if session['role'] != 'admin':
        return jsonify({"success": False, "message": "Only admin users can perform this action."}), 403
    data = request.json
    if not data or 'product_id' not in data or 'new_price' not in data:
        return jsonify({"success": False, "message": "Invalid input."}), 400
    result = ProductService.update_price_by_id(data['product_id'], data['new_price'])
    return jsonify(result), (200 if result["success"] else 500)

@app.route('/product', methods=['DELETE'])
def delete_product_by_id():
    # delete product
    # the request.json should include product_id
    if 'token' not in session:
        return redirect(url_for('index'))
    if session['role'] != 'admin':
        return jsonify({"success": False, "message": "Only admin users can perform this action."}), 403
    data = request.json
    if not data or 'product_id' not in data:
        return jsonify({"success": False, "message": "Invalid input."}), 400
    result = ProductService.delete_product_by_id(data['product_id'])
    return jsonify(result), (200 if result["success"] else 500)