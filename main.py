import os
from flask import Flask, jsonify, request, g
from app.users.users_route import users_controller
from app.workspaces.workspaces_route import workspaces_controller
from app.cashflows.cashflows_route import cashflows_controller
import jwt
from common.config import config
from flask_cors import CORS
from common.middleware import Middleware

app = Flask(__name__)
CORS(app)

app.register_blueprint(users_controller, url_prefix='/users')
app.register_blueprint(workspaces_controller, url_prefix='/workspaces')
app.register_blueprint(cashflows_controller, url_prefix='/cashflows')


@app.before_request
def load_user():
    middlware = Middleware()
    return middlware.bearerAuth()


@app.route('/')
def welcome():
    return jsonify({'message': 'hello world'})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
