from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import os

app = Flask(__name__)

# MongoDB connection setup
mongo_conn_str = os.environ.get('MONGO_CONN_STR')
client = MongoClient(mongo_conn_str)
db = client.LightingStoreDB

@app.route('/')
def home():
    return 'Welcome to the Lighting Store API!'

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

if __name__ == '__main__':
    app.run(debug=True)