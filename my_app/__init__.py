import os
from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True) 

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # --- REGISTRE SEUS BLUEPRINTS AQUI ---
    # Importe os blueprints *dentro* da factory para evitar importação circular
    
    # Exemplo de como você registraria o blueprint de pets:
    # from .api.pets import pets_bp 
    # app.register_blueprint(pets_bp, url_prefix='/api/v1/pets')

    # Exemplo para donos:
    # from .api.donos import donos_bp
    # app.register_blueprint(donos_bp, url_prefix='/api/v1/donos')


    # Uma rota simples de "health check"
    @app.route('/health')
    def health_check():
        return "OK", 200
    
    return app