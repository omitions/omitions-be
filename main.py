import os
from flask import Flask, jsonify
from app.auths.routes import auths_bp
from app.users.routes import users_bp

app = Flask(__name__)

app.register_blueprint(auths_bp, url_prefix='/auths')
app.register_blueprint(users_bp, url_prefix='/users')


@app.route('/')
def welcome():
    return jsonify({'message': 'hello world'})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
