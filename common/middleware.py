from flask import request, jsonify, g
from common.config import config

import jwt

middleware_auth_excludes = [
    '/users/login',
    '/users/register',
    '/',
    '/users/forgot-password'
]


class Middleware:
    def bearerAuth(self):
        print(request.path)
        if request.path in middleware_auth_excludes:
            return
        try:
            if not request.headers.get('Authorization'):
                return jsonify({'message': 'Authorization header is required'}), 401

            token = request.headers.get('Authorization').split(' ')[1]
            if not token:
                return jsonify({'message': 'Token not found'}), 401

            users = jwt.decode(
                token, config['PROD']['JWT_SECRET'], algorithms=["HS256"])
            g.user = users
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Expired signature'}), 401
        except jwt.InvalidSignatureError:
            return jsonify({'message': 'Invalid signature'}), 401
        except Exception as e:
            print("An unexpected error occurred:", e)
            return jsonify({'message': 'Invalid signature'}), 401
