from flask import Blueprint, jsonify
from common.database import mongo

auths_bp = Blueprint('auths', __name__)


@auths_bp.route('/login', methods=['POST'])
def login():
    mongo.db.auths.insert_one({'username': 'user1'})
    return jsonify({'message': 'Login endpoint'})


@auths_bp.route('/logout', methods=['POST'])
def logout():
    # Implement your logout logic here
    return jsonify({'message': 'Logout endpoint'})

# Anda bisa menambahkan rute lainnya di sini
