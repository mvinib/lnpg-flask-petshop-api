from flask import Blueprint, jsonify, request
from ..services.appointments import Appointments
from ..utils.validate import schemaValidate

appointments_bp = Blueprint('appointments', __name__)

@appointments_bp.route('/', methods=['GET'])
def get_Appointments():
    appointments = Appointments()
    filters = request.args.to_dict()
    
    appointments = Appointments()
    data = []

    if not filters:
        data = appointments.list()
    else:
        data = appointments.search(filters)

    return jsonify({
        "success": True,
        "data": data
    }), 200

@appointments_bp.route('/<int:appointment_id>', methods=['GET'])
def get_appointment_by_id(appointment_id):
    appointments = Appointments()
    appointment = appointments.get_by_id(appointment_id)
    if appointment: 
        return jsonify({
            "success": True,
            "data": appointment
        }), 200
    
    return jsonify({
        "success": False,
        "point": "get_appointment_by_id",
        "message": "Agendamento não encontrado"
    }), 404


@appointments_bp.route('/', methods=['POST'])
def create_appointment():
    data = request.json

    validation_error = schemaValidate(["pet_id", "service_id", "employee_id", "scheduled_at"], data)

    if validation_error:
        return validation_error
    
    appointments = Appointments()
    try:
        appointments.create(data)
    except Exception as err:
        return jsonify({
            "success": False,
            "point": "create_appointment",
            "message": str(err)
        }), 400

    return jsonify({ "success": True }), 201

@appointments_bp.route('/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    appointments = Appointments()
    try:
        appointments.delete(appointment_id)
    except Exception as err:
        return jsonify({
            "success": False,
            "point": "delete_appointment",
            "message": str(err)
        }), 400
    
    return jsonify({ "success": True }), 200

@appointments_bp.route('/<int:appointment_id>', methods=['PATCH'])
def update_appointment(appointment_id):
    data = request.json
    validation_error = schemaValidate(["id", "pet_id"], data, False)

    if validation_error:
        return validation_error
    
    status = data.get("status", None)
    if status:
        status_allowed = ["scheduled", "finished", "canceled"]
        if status not in status_allowed:
            return jsonify({
            "success": False,
            "point": "update_appointment",
            "message": f"O status informado é inválido. Valores válidos: {", ".join(status_allowed)}"
        }), 422
    
    appointments = Appointments()
    try:
        appointments.update(appointment_id, data)
    except Exception as err:

        return jsonify({
            "success": False,
            "point": "update_appointment",
            "message": str(err)
        }), 400
    
    return jsonify({ "success": True }), 200

        