from flask import Blueprint, jsonify, request
from ..services.services import Services
from ..utils.validate import schemaValidate

services_bp = Blueprint('services', __name__)

@clients_bp.route('/', methods=['GET'])
def get_services():
    services = Services()
    filters = request.args.to_dict()
    
    services = Services()
    data = []

    if not filters:
        data = services.list()
    else:
        data = services.search(filters)

    return jsonify({
        "success": True,
        "data": data
    }), 200

@services_bp.route('/<int:service_id>', methods=['GET'])
def get_service_by_id(service_id):
    services = Services()
    services = services.get_by_id(service_id)
    if service: 
        return jsonify({
            "success": True,
            "data": service
        }), 200
    
    return jsonify({
        "success": False,
        "point": "get_service_by_id",
        "message": "Serviço não encontrado"
    }), 404


@services_bp.route('/', methods=['POST'])
def create_service():
    data = request.json

    validation_error = schemaValidate(["name", "description", "value"], data)

    if validation_error:
        return validation_error
    
    services = Services()
    services.create(data)

    return jsonify({ "success": True }), 201

@services_bp.route('/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    services = Services()
    try:
        services.delete(service_id)
    except Exception as err:

        return jsonify({
            "success": False,
            "point": "delete_service",
            "message": str(err)
        }), 400
    
    return jsonify({ "success": True }), 200

@services_bp.route('/<int:service_id>', methods=['PATCH'])
def update_service(service_id):
    data = request.json
    validation_error = schemaValidate(["id", "created_at"], data, False)

    if validation_error:
        return validation_error
    
    services = Services()
    try:
        services.update(service_id, data)
    except Exception as err:

        return jsonify({
            "success": False,
            "point": "update_service",
            "message": str(err)
        }), 400
    
    return jsonify({ "success": True }), 200

        