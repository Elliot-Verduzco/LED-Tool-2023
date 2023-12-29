# routes.py
from app import db, User
from flask import Flask, jsonify, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

def create_routes(app, db, User):
    @app.route('/')
    def home():
        return 'Welcome to the Lighting Store API!'

    @app.route('/register', methods=['POST'])
    def register():
        username = request.json.get('username')
        password = request.json.get('password')
        # Ensure username is unique and password is not empty
        if username and password and db.users.find_one({'username': username}) is None:
            # Hash the user's password
            hashed_pw = generate_password_hash(password)
            user_id = db.users.insert_one({'username': username, 'password': hashed_pw}).inserted_id
            return jsonify({'message': 'User created successfully', 'user_id': str(user_id)}), 201
        else:
            return jsonify({'message': 'Username already exists or password is empty'}), 400

    @app.route('/login', methods=['POST'])
    def login():
        username = request.json.get('username')
        password = request.json.get('password')
        user = db.users.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            user_obj = User(user['_id'])
            login_user(user_obj)
            return jsonify({'message': 'Logged in successfully'}), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401

    @app.route('/logout', methods=['GET'])
    @login_required
    def logout():
        logout_user()
        return jsonify({'message': 'Logged out successfully'}), 200

    @app.route('/protected', methods=['GET'])
    @login_required
    def protected():
        return jsonify({'message': 'This is a protected route.'}), 200

    @app.route('/add_order', methods=['POST'])
    def add_order():
        order_data = request.json  # Assuming the order data is sent in JSON format
        db.orders.insert_one(order_data)  # 'orders' is the collection in your MongoDB
        return jsonify({'message': 'Order added successfully'}), 201

    @app.route('/orders', methods=['GET'])
    def get_orders():
        orders = db.orders.find()  # Retrieves all documents from the 'orders' collection
        return jsonify([order for order in orders]), 200

    @app.route('/order/<order_id>', methods=['GET'])
    def get_order(order_id):
        order = db.orders.find_one({'_id': order_id})
        if order:
            return jsonify(order), 200
        else:
            return jsonify({'message': 'Order not found'}), 404

    @app.route('/update_order/<order_id>', methods=['PUT'])
    def update_order(order_id):
        update_data = request.json
        db.orders.update_one({'_id': order_id}, {'$set': update_data})
        return jsonify({'message': 'Order updated successfully'}), 200

    @app.route('/delete_order/<order_id>', methods=['DELETE'])
    def delete_order(order_id):
        db.orders.delete_one({'_id': order_id})
        return jsonify({'message': 'Order deleted successfully'}), 200

    @app.route('/test_db')
    def test_db():
        try:
            # Attempt to fetch a list of all collections in the database
            collections = db.list_collection_names()
            return jsonify({'collections': collections}), 200
        except Exception as e:
            # If an error occurs, return the error message
            return jsonify({'error': str(e)}), 500

    # Return the app object for further use
    return app