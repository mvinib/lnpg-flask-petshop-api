from flask import Blueprint, jsonify, request
from ..services.clients import Clients
from ..utils.validate import schemaValidate
from flask_jwt_extended import jwt_required

clients_bp = Blueprint('clients', __name__)

@clients_bp.route('/', methods=['GET'])
def get_clients():
    clients = Clients()
    filters = request.args.to_dict()
    
    clients = Clients()
    data = []

    if not filters:
        data = clients.list()
    else:
        data = clients.search(filters)

    return jsonify({
        "success": True,
        "data": data
    }), 200

@clients_bp.route('/<int:client_id>', methods=['GET'])
def get_client_by_id(client_id):
    clients = Clients()
    client = clients.get_by_id(client_id)
    if client: 
        return jsonify({
            "success": True,
            "data": client
        }), 200
    
    return jsonify({
        "success": False,
        "point": "get_client_by_id",
        "message": "Cliente não encontrado"
    }), 404


@clients_bp.route('/', methods=['POST'])
def create_client():
    data = request.json

    validation_error = schemaValidate(["name", "phone", "email"], data)

    if validation_error:
        return validation_error
    
    clients = Clients()
    try:
        clients.create(data)
    except Exception as err:
        return jsonify({
            "success": False,
            "point": "create_client",
            "message": str(err)
        }), 400
    

    return jsonify({ "success": True }), 201

@clients_bp.route('/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    clients = Clients()
    try:
        clients.delete(client_id)
    except Exception as err:

        return jsonify({
            "success": False,
            "point": "delete_client",
            "message": str(err)
        }), 400
    
    return jsonify({ "success": True }), 200

@clients_bp.route('/<int:client_id>', methods=['PATCH'])
def update_client(client_id):
    data = request.json
    validation_error = schemaValidate(["id", "created_at"], data, False)

    if validation_error:
        return validation_error
    
    clients = Clients()
    try:
        clients.update(client_id, data)
    except Exception as err:

        return jsonify({
            "success": False,
            "point": "update_client",
            "message": str(err)
        }), 400
    
    return jsonify({ "success": True }), 200

        