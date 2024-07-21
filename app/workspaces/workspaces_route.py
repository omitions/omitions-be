from flask import Blueprint, request
from app.workspaces.workspaces_service import CashflowsService

workspaces_controller = Blueprint('workspaces', __name__)
workspaces_service = CashflowsService()


@workspaces_controller.route('/create', methods=['POST'])
def create():
    return workspaces_service.create(request)


@workspaces_controller.route('/update', methods=['POST'])
def update():
    return workspaces_service.update(request)
