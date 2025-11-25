from flask import jsonify, request
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from ..services.services import Services
from ..utils.validate import schemaValidate, ValidationFailedSchema
from ..schemas.generic import GenericSuccessSchema
from ..schemas.service import (
    GetServicesResponseSchema,
    GetServiceByIDResponseSchema,
    GetServiceByIDResponseNotFoundSchema,
    CreateServiceSchema,
    CreateServiceResponseFailedSchema,
    UpdateServiceSchema,
    UpdateServiceResponseFailedSchema,
    DeleteServiceResponseFailedSchema
)

services_bp = Blueprint('services', __name__, description="Gestão de Serviços")

@services_bp.route('/', methods=['GET'])
@services_bp.response(200, GetServicesResponseSchema, description="Listar serviços")
@services_bp.doc(security=[{"bearerAuth": []}])
@jwt_required()
def get_services():
    """Buscar lista de serviços
    """
    services = Services()
    filters = request.args.to_dict()
    data = []

    if not filters:
        data = services.list()
    else:
        data = services.search(filters)

    return jsonify({"success": True, "data": data}), 200

@services_bp.route('/<id>', methods=['GET'])
@services_bp.response(200, GetServiceByIDResponseSchema, description="Serviço encontrado")
@services_bp.response(404, GetServiceByIDResponseNotFoundSchema, description="Serviço não encontrado")
@services_bp.doc(security=[{"bearerAuth": []}])
@jwt_required()
def get_service_by_id(id):
    """Buscar serviço pelo ID
    """
    services = Services()
    service = services.get_by_id(id)
    if service: 
        return jsonify({"success": True, "data": service}), 200
    
    return jsonify({"success": False, "point": "get_service_by_id", "message": "Serviço não encontrado"}), 404

@services_bp.route('/', methods=['POST'])
@services_bp.doc(
    security=[{"bearerAuth": []}],
    requestBody={
        "content": {
            "application/json": {
                "schema": CreateServiceSchema
            }
        }
    }
)
@services_bp.response(201, GenericSuccessSchema, description="Serviço criado com sucesso")
@services_bp.response(400, CreateServiceResponseFailedSchema, description="Falha ao criar o serviço")
@services_bp.response(422, ValidationFailedSchema, description="Falha na validação dos campos")
@jwt_required()
def create_service():
    """Criar novo serviço
    """
    data = request.json
    validation_error = schemaValidate(["name", "description", "value"], data)

    if validation_error: return validation_error
    
    services = Services()
    try:
        services.create(data)
    except Exception as err:
        return jsonify({"success": False, "point": "create_service", "message": str(err)}), 400

    return jsonify({ "success": True }), 201

@services_bp.route('/<id>', methods=['DELETE'])
@services_bp.doc(security=[{"bearerAuth": []}])
@services_bp.response(200, GenericSuccessSchema, description="Serviço deletado com sucesso")
@services_bp.response(400, DeleteServiceResponseFailedSchema, description="Serviço não encontrado")
@jwt_required()
def delete_service(id):
    """Deletar serviço
    """
    services = Services()
    try:
        services.delete(id)
    except Exception as err:
        return jsonify({"success": False, "point": "delete_service", "message": str(err)}), 400
    
    return jsonify({ "success": True }), 200

@services_bp.route('/<id>', methods=['PATCH'])
@services_bp.doc(
    security=[{"bearerAuth": []}], 
    requestBody={
        "content": {
            "application/json": {
                "schema": UpdateServiceSchema
            }
        }
    }
)
@services_bp.response(200, GenericSuccessSchema, description="Serviço editado com sucesso")
@services_bp.response(400, UpdateServiceResponseFailedSchema, description="Serviço não encontrado")
@services_bp.response(422, ValidationFailedSchema, description="Falha na validação dos campos")
@jwt_required()
def update_service(id):
    """Editar serviço
    """
    data = request.json
    validation_error = schemaValidate(["id", "created_at"], data, False)

    if validation_error: return validation_error
    
    services = Services()
    try:
        services.update(id, data)
    except Exception as err:
        return jsonify({"success": False, "point": "update_service", "message": str(err)}), 400
    
    return jsonify({ "success": True }), 200