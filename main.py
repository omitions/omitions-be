import os
from flask import Flask, jsonify, request, g
from app.users.users_route import users_controller
from app.workspaces.workspaces_route import workspaces_controller
import jwt
from common.config import config

app = Flask(__name__)

app.register_blueprint(users_controller, url_prefix='/users')
app.register_blueprint(workspaces_controller, url_prefix='/workspaces')

middleware_auth_excludes = [
    '/users/login',
    '/users/register',
]


@app.before_request
def load_user():
    if request.path in middleware_auth_excludes:
        return
    try:
        if not request.headers.get('Authorization'):
            return jsonify({'message': 'Authorization header is required'}), 401
        print(request.headers.get('Authorization'))
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


@app.route('/')
def welcome():
    return jsonify({'message': 'hello world'})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
