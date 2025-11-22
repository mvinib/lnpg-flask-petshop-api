from flask import Blueprint, jsonify, request
from ..services.employees import Employees
from ..utils.validate import schemaValidate
from flask_jwt_extended import jwt_required

employees_bp = Blueprint('employees', __name__)

@employees_bp.route('/', methods=['GET'])
@jwt_required()
def get_employees():
    employees = Employees()
    filters = request.args.to_dict()
    
    employees = Employees()
    data = []

    if not filters:
        data = employees.list()
    else:
        data = employees.search(filters)

    return jsonify({
        "success": True,
        "data": data
    }), 200

@employees_bp.route('/<int:employee_id>', methods=['GET'])
@jwt_required()
def get_employee_by_id(employee_id):
    employees = Employees()
    employee = employees.get_by_id(employee_id)
    if employee: 
        return jsonify({
            "success": True,
            "data": employee
        }), 200
    
    return jsonify({
        "success": False,
        "point": "get_employee_by_id",
        "message": "Funcionário não encontrado"
    }), 404


@employees_bp.route('/', methods=['POST'])
@jwt_required()
def create_employee():
    data = request.json

    validation_error = schemaValidate(["name", "job_title", "email", "password"], data)

    if validation_error:
        return validation_error
    
    employees = Employees()
    employees.create(data)

    return jsonify({ "success": True }), 201

@employees_bp.route('/<int:employee_id>', methods=['DELETE'])
@jwt_required()
def delete_employee(employee_id):
    employees = Employees()
    try:
        employees.delete(employee_id)
    except Exception as err:

        return jsonify({
            "success": False,
            "point": "delete_employee",
            "message": str(err)
        }), 400
    
    return jsonify({ "success": True }), 200

@employees_bp.route('/<int:employee_id>', methods=['PATCH'])
@jwt_required()
def update_employee(employee_id):
    data = request.json
    validation_error = schemaValidate(["id", "created_at"], data, False)

    if validation_error:
        return validation_error
    
    employees = Employees()
    try:
        employees.update(employee_id, data)
    except Exception as err:

        return jsonify({
            "success": False,
            "point": "update_employee",
            "message": str(err)
        }), 400
    
    return jsonify({ "success": True }), 200

        