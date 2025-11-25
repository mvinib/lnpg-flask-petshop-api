from flask import jsonify, request
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from ..services.pets import Pets
from ..schemas.generic import GenericSuccessSchema
from ..utils.validate import schemaValidate

# Import dos Schemas
from ..schemas.pets import (
    GetPetsResponseSchema, GetPetsByIDResponseSchema, GetPetsByIDResponseNotFoundSchema,
    CreatePetSchema, CreatePetResponseFailedSchema,
    DeletePetResponseFailedSchema,
    UpdatePetSchema, UpdatePetResponseFailedSchema,
    PetFilterSchema, # <--- IMPORT NOVO
    VALID_SPECIES
)

# Tenta importar o ValidationFailedSchema
try:
    from ..utils.validate import ValidationFailedSchema
except ImportError:
    ValidationFailedSchema = None

pets_bp = Blueprint('pets', __name__)

# -----------------------------------------------------------------------------
# ROTA: LISTAR PETS (Atualizada com Filtros)
# -----------------------------------------------------------------------------
@pets_bp.route('/', methods=['GET'])
@pets_bp.response(200, GetPetsResponseSchema, description="Lista de pets recuperada com sucesso")
@pets_bp.arguments(PetFilterSchema, location="query") # <--- Injeta os filtros na função
@pets_bp.doc(security=[{"bearerAuth": []}])
@jwt_required()
def get_pets(filters): # Recebe 'filters' do argumento acima
    """Listar todos os pets.

    Retorna uma listagem completa dos animais cadastrados.
    Permite filtros avançados via Query Parameters (logic, operator, etc).
    """
    pets = Pets()
    data = []

    # Se o filtro tiver APENAS 'logic' e 'operator' (que são padrões), listamos tudo.
    # Se tiver mais chaves (name, specie...), fazemos a busca.
    keys_de_busca = [k for k in filters.keys() if k not in ["logic", "operator"]]
    
    if not keys_de_busca:
        data = pets.list()
    else:
        data = pets.search(filters)

    return jsonify({"success": True, "data": data}), 200

# -----------------------------------------------------------------------------
# ROTA: BUSCAR PET POR ID
# -----------------------------------------------------------------------------
@pets_bp.route('/<int:pet_id>', methods=['GET'])
@pets_bp.response(200, GetPetsByIDResponseSchema, description="Pet encontrado")
@pets_bp.response(404, GetPetsByIDResponseNotFoundSchema, description="ID não encontrado no sistema")
@pets_bp.doc(security=[{"bearerAuth": []}])
@jwt_required()
def get_pet_by_id(pet_id):
    """Obter detalhes de um pet."""
    pets = Pets()
    pet = pets.get_by_id(pet_id)

    if pet:
        return jsonify({"success": True, "data": pet}), 200

    return jsonify({
        "success": False,
        "point": "get_pet_by_id",
        "message": "Pet não encontrado"
    }), 404

# -----------------------------------------------------------------------------
# ROTA: CRIAR PET
# -----------------------------------------------------------------------------
@pets_bp.route('/', methods=['POST'])
@pets_bp.doc(security=[{"bearerAuth": []}])
@pets_bp.doc(
    requestBody={
        "content": {
            "application/json": {
                "schema": CreatePetSchema 
            }
        },
        "required": True 
    }
)
@pets_bp.response(201, GenericSuccessSchema, description="Pet cadastrado com sucesso")
@pets_bp.response(400, CreatePetResponseFailedSchema, description="Violação de regra de negócio")
@pets_bp.response(422, ValidationFailedSchema, description="Erro de validação")
@jwt_required()
def create_pet(): 
    """Cadastrar novo pet."""
    pet_data = request.json

    validation_error = schemaValidate(["name", "specie", "age", "owner_id", "sex"], pet_data)

    if validation_error:
        return validation_error
    
    if not pet_data.get("specie") in VALID_SPECIES:
        return jsonify({
            "success": False,
            "point": "create_pet_validation",
            "message": f"O campo 'specie' deve ser {", ".join(VALID_SPECIES)}"
        }), 400

    if pet_data["sex"].upper() not in ('M', 'F'):
        return jsonify({
            "success": False,
            "point": "create_pet_validation",
            "message": "O campo 'sex' deve ser 'M' (Macho) ou 'F' (Fêmea)."
        }), 400
    
    pet_data["sex"] = pet_data["sex"].upper()

    pets = Pets()
    try:
        pets.create(pet_data)
    except Exception as err:
        return jsonify({
            "success": False,
            "point": "create_pet",
            "message": str(err)
        }), 400

    return jsonify({"success": True}), 201

# -----------------------------------------------------------------------------
# ROTA: ATUALIZAR PET
# -----------------------------------------------------------------------------
@pets_bp.route('/<int:pet_id>', methods=['PATCH'])
@pets_bp.doc(security=[{"bearerAuth": []}])
@pets_bp.doc(
    requestBody={
        "content": {
            "application/json": {
                "schema": UpdatePetSchema 
            }
        },
        "required": True 
    }
)
@pets_bp.response(200, GenericSuccessSchema, description="Atualização realizada")
@pets_bp.response(400, UpdatePetResponseFailedSchema, description="Erro na atualização")
@pets_bp.response(422, ValidationFailedSchema, description="Formato de dados inválido")
@jwt_required()
def update_pet(pet_id): 
    """Atualizar dados do pet."""
    pet_data = request.json

    validation_error = schemaValidate(["id", "created_at"], pet_data, False)

    if validation_error:
        return validation_error
    
    if "sex" in pet_data:
        sex = pet_data.get("sex")
        if sex:
            if sex.upper() not in ('M', 'F'):
                return jsonify({
                    "success": False,
                    "point": "update_pet_validation",
                    "message": "O campo 'sex' deve ser 'M' (Macho) ou 'F' (Fêmea)."
                }), 400
            pet_data["sex"] = sex.upper()
    if "specie" in pet_data:
        if not pet_data.get("specie") in VALID_SPECIES:
            return jsonify({
                "success": False,
                "point": "create_pet_validation",
                "message": f"O campo 'specie' deve ser {", ".join(VALID_SPECIES)}"
            }), 400

    pets = Pets()
    try:
        pets.update(pet_id, pet_data)
    except Exception as err:
        return jsonify({
            "success": False,
            "point": "update_pet",
            "message": str(err)
        }), 400

    return jsonify({"success": True}), 200

# -----------------------------------------------------------------------------
# ROTA: DELETAR PET
# -----------------------------------------------------------------------------
@pets_bp.route('/<int:pet_id>', methods=['DELETE'])
@pets_bp.doc(security=[{"bearerAuth": []}])
@pets_bp.response(200, GenericSuccessSchema, description="Registro removido")
@pets_bp.response(400, DeletePetResponseFailedSchema, description="ID não encontrado ou erro ao deletar")
@jwt_required()
def delete_pet(pet_id):
    """Remover pet do sistema."""
    pets = Pets()
    try:
        pets.delete(pet_id)
    except Exception as err:
        return jsonify({
            "success": False,
            "point": "delete_pet",
            "message": str(err)
        }), 400

    return jsonify({"success": True}), 200