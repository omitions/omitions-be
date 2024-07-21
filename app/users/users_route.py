from flask import Blueprint, request, g
from app.users.users_service import UsersService

users_controller = Blueprint('users', __name__)
users_service = UsersService()


@users_controller.route('/register', methods=['POST'])
def register():
    return users_service.register(request)


@users_controller.route('/login', methods=['POST'])
def login():
    return users_service.login(request)


@users_controller.route('/logout', methods=['POST'])
def logout():
    return users_service.logout(request)


@users_controller.route('/profile', methods=['GET'])
def profile():
    print(g.user)
    return users_service.profile(request)
