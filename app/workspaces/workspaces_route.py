from flask import Blueprint, request
from app.workspaces.workspaces_service import WorkspacesService

workspaces_controller = Blueprint('workspaces', __name__)
workspaces_service = WorkspacesService()


@workspaces_controller.route('/create', methods=['POST'])
def create():
    return workspaces_service.create(request)


@workspaces_controller.route('/update', methods=['POST'])
def update():
    return workspaces_service.update(request)

@workspaces_controller.route('/delete', methods=['POST'])
def delete():
    return workspaces_service.delete(request)

@workspaces_controller.route('/list', methods=['GET'])
def list():
    return workspaces_service.list(request)
