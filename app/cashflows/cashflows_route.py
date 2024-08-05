from flask import Blueprint, request
from app.cashflows.cashflows_service import CashflowsService

cashflows_controller = Blueprint('cashflows', __name__)
cashflows_service = CashflowsService()


@cashflows_controller.route('/create', methods=['POST'])
def create():
    return cashflows_service.create(request)


@cashflows_controller.route('/update', methods=['POST'])
def update():
    return cashflows_service.update(request)


@cashflows_controller.route('/list', methods=['GET'])
def list():
    return cashflows_service.list(request)
