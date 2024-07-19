from flask import Blueprint, jsonify, request
from common.database import mongo
from app.users.services.user_register import Registration
from bson import ObjectId
import json

users_bp = Blueprint('users', __name__)


@users_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data:
        return jsonify({'message': 'Data JSON tidak ditemukan'}), 400

    fullname = data.get('fullname')
    password = data.get('password')
    email = data.get('email')

    if not fullname or not password or not email:
        return jsonify({'message': 'Mohon masukkan fullname, password, dan email'}), 400

    user_data = {
        'fullname': fullname,
        'password': password,
        'email': email
    }

    result = mongo.db['users'].insert_one(user_data)
    if result.inserted_id:
        return jsonify({'message': 'User added successfully', 'id': str(result.inserted_id)})
    else:
        return jsonify({'message': 'Failed to add user'}), 500
    return jsonify(user_data)


@users_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = {'id': user_id, 'fullname': 'user{}'.format(user_id)}
    return jsonify(user)
