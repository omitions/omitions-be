import json
import bcrypt
import jwt
import smtplib
from common.database import mongo
from flask import jsonify, g
from common.config import config
from bson import json_util, ObjectId
from common.utils import Utils
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template


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

    def forgot_password(self, request):
        email = request.json.get("email")
        user = mongo.db['users'].find_one({"email": email})
        if not user:
            return jsonify({'message': 'User not found'}), 404

        generate_token_5_minutes = jwt.encode(
            {
                "_id": str(user.get("_id")),
                "email": email,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
            },
            self.jwt_secret, algorithm='HS256'
        )

        email_from = 'toto.rubianto.19@gmail.com'
        email_password = 'fojb gwjw iqtf bohd'
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587

        # Email content
        subject = 'Reset password mybucks.today'
        token = str(generate_token_5_minutes)
        reset_url = f'https://mybucks.today/forgot-password?token={token}'

        # Template Jinja2
        template_string = """
        <html>
        <body>
            <p>Halo,</p>
            <p>Kami menerima permintaan untuk mengatur ulang kata sandi Anda.</p>
            <p>Silakan klik tautan di bawah ini untuk membuat kata sandi baru:</p>
            <a href="{{ reset_url }}">{{ reset_url }}</a>
            <p>Jika Anda tidak meminta pengaturan ulang kata sandi, abaikan email ini.</p>
        </body>
        </html>
        """

        template = Template(template_string)
        html_content = template.render(reset_url=reset_url)

        message = MIMEMultipart()
        message['From'] = email_from
        message['To'] = email
        message['Subject'] = subject

        message.attach(MIMEText(html_content, 'html'))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Enable TLS encryption
            server.login(email_from, email_password)
            server.sendmail(email_from, email, message.as_string())

        return jsonify({'message': "success, please check email!"})

    def reset_password(self, request):
        user_id = g.user["_id"]
        req_json = self.utils_helper.parse_json(request.json)
        if not req_json:
            return jsonify({'message': 'Data not valid!'}), 400

        if req_json['new_password'] != req_json['new_password_confirmation']:
            return jsonify({'message': 'Password not match!'}), 400

        new_password = self.utils_helper.hash_password(
            req_json["new_password"])
        mongo.db['users'].update_one(
            {"_id": ObjectId(user_id)}, {"$set": {"password": new_password}})
        return jsonify({'message': "success"})

    def change_password(self, request):
        user_id = g.user["_id"]
        req_json = self.utils_helper.parse_json(request.json)
        if not req_json:
            return jsonify({'message': 'Data not valid!'}), 400

        if req_json['new_password'] != req_json['new_password_confirmation']:
            return jsonify({'message': 'Password not match!'}), 400

        user = mongo.db['users'].find_one({'_id': ObjectId(user_id)})
        if not user:
            return jsonify({'message': 'user notfound'}), 400

        new_password = req_json["new_password"]
        match = bcrypt.checkpw(new_password, user.get(password))
        if not match:
            return jsonify({'message': 'password doest match!'}), 400

        new_password = self.utils_helper.hash_password(new_password)
        mongo.db['users'].update_one(
            {"_id": ObjectId(user_id)}, {"$set": {"password": new_password}})

        return jsonify({'message': "success"})
