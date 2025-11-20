import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from datetime import timedelta

def create_app():
    load_dotenv()
    app = Flask(__name__, instance_relative_config=True) 
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=1)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .api.clients import clients_bp
    from .api.appointments import appointments_bp
    from .api.pets import pets_bp
    from .api.employees import employees_bp
    from .api.auth import auth_bp

    app.register_blueprint(clients_bp, url_prefix='/clients')
    app.register_blueprint(appointments_bp, url_prefix='/appointments')
    app.register_blueprint(pets_bp, url_prefix='/pets')
    app.register_blueprint(employees_bp, url_prefix='/employees')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    jwt = JWTManager(app)
    @jwt.unauthorized_loader
    def custom_unauthorized_response(err):
        return jsonify({
            "success": False,
            "point": "authentication",
            "message": "Envie um header Authorization"
        }), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload): 
        token_type = jwt_payload.get('type', 'access')
        
        if token_type == 'refresh':
            return jsonify({
                "success": False,
                "point": "renew_token",
                "message": "Sessão expirada. Faça login novamente."
            }), 401
        
        return jsonify({
            "success": False,
            "message": "Token de acesso expirado. Use o refresh token para obter um novo.",
            "point": "access_token_expired"
        }), 401
    
    @app.route('/health')
    def health_check():
        return "OK", 200
    
    return app