from flask import Blueprint, jsonify, request
from common.database import mongo
from app.users.services.user_register import Registration

users_bp = Blueprint('users', __name__)


@users_bp.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    user_data = {
        'username': username,
        'password': password,
        'email': email
    }
    # registration = Registration(user_data)
    print(username, password)
    mongo.db.users.insert_one(user_data)
    return jsonify(user_data)


@users_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = {'id': user_id, 'username': 'user{}'.format(user_id)}
    return jsonify(user)
