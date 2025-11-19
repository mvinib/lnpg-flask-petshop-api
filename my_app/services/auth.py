from .employees import Employees
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token

class Auth:    
    def login(self, data: dict):
        email = data.get("email")
        password = data.get("password")
        employees = Employees()

        employee = employees.search({
            "email": email
        })

        if employee and check_password_hash(employee[0].get("password", None), password):
            user_data = employee[0]
            user_id = user_data.get("id")

            additional_claims = {
                "user_id": user_id,
                "email": email
            }
            access_token = create_access_token(
                identity=user_id,
                additional_claims=additional_claims
            )

            refresh_token = create_refresh_token(identity=user_id)
        
            return {"access_token": access_token, "refresh_token": refresh_token }

        raise Exception("Credenciais de acesso incorretas")