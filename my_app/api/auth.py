from flask import Blueprint, jsonify, request
from ..services.auth import Auth
from ..utils.validate import schemaValidate
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json

    validation_error = schemaValidate(["email", "password"], data)

    if validation_error:
        return validation_error
    
    auth = Auth()
    try:
        response = auth.login(data)
        return response, 200
    except Exception as err:
        return jsonify({
            "success": False,
            "point": "login",
            "message": str(err)
        }), 400

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    
    return {"access_token": new_access_token}, 200

        