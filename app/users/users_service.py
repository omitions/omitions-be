from common.database import mongo
import json
from flask import jsonify, g
import bcrypt
from common.config import config
import jwt
from bson import json_util, ObjectId
from common.utils import Utils


class UsersService:
    def __init__(self):
        self.utils_helper = Utils()
        self.jwt_secret = config['PROD']['JWT_SECRET']

    def register(self, request):
        data = request.json
        if not data:
            return jsonify({'message': 'Data JSON tidak ditemukan'}), 400

        fullname = data.get('fullname')
        password = data.get('password')
        email = data.get('email')

        user = mongo.db['users'].find_one({"email": email})
        if user:
            return jsonify({'message': 'User already exists'}), 409

        if not fullname or not password or not email:
            return jsonify({'message': 'Mohon masukkan fullname, password, dan email'}), 400

        user_data = {
            'fullname': fullname,
            'password': self.utils_helper.hash_password(password),
            'email': email
        }

        result = mongo.db['users'].insert_one(user_data)
        if result.inserted_id:
            return jsonify({'message': 'User added successfully', 'id': str(result.inserted_id)})
        else:
            return jsonify({'message': 'Failed to add user'}), 500

    def login(self, request):
        data = request.json
        if not data:
            return jsonify({'message': 'Data JSON tidak ditemukan'}), 400

        email = data.get('email')
        password = data.get('password')
        user = mongo.db['users'].find_one({"email": email})
        if not user:
            return jsonify({'message': 'User not found'}), 404

        valid = self.utils_helper.verify_password(
            user.get("password"), password)
        if not valid:
            return jsonify({'message': 'Wrong password'}), 401
        payload = {
            '_id': str(user.get("_id")),
            'fullname': user.get('fullname'),
            'email': user.get('email')
        }
        token = jwt.encode(payload, self.jwt_secret, algorithm='HS256')
        return jsonify({
            'message': 'User logged in successfully',
            'data': {'access_token': token}
        })

    def logout(self, request):
        return "true"

    def profile(self, request):
        user = mongo.db['users'].find_one({"_id": ObjectId(g.user['_id'])})
        if not user:
            return jsonify({'message': 'User not found'}), 404
        return jsonify(self.utils_helper.parse_json(user))
