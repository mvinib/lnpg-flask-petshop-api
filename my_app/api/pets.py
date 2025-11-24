from flask import jsonify, request
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from ..services.pets import Pets
from ..schemas.generic import GenericSuccessSchema

# Import dos Schemas
from ..schemas.pets import (
    GetPetsResponseSchema, GetPetsByIDResponseSchema, GetPetsByIDResponseNotFoundSchema,
    CreatePetSchema, CreatePetResponseFailedSchema,
    DeletePetResponseFailedSchema,
    UpdatePetSchema, UpdatePetResponseFailedSchema,
)

# Tenta importar o ValidationFailedSchema, senão usa o padrão do erro 422
try:
    from ..utils.validate import ValidationFailedSchema
except ImportError:
    ValidationFailedSchema = None

pets_bp = Blueprint('pets', __name__)

# -----------------------------------------------------------------------------
# ROTA: LISTAR PETS
# -----------------------------------------------------------------------------
@pets_bp.route('/', methods=['GET'])
@pets_bp.response(200, GetPetsResponseSchema, description="Lista de pets recuperada com sucesso")
@pets_bp.doc(security=[{"bearerAuth": []}])
@jwt_required()
def get_pets():
    """Listar todos os pets.

    Retorna uma listagem completa dos animais cadastrados.
    
    **Funcionalidades:**
    * **Filtros:** É possível filtrar por qualquer campo (ex: `?specie=Cachorro&sex=M`).
    * **Relacionamento:** Cada pet traz o objeto completo do seu Dono (`owner_id`).
    """
    pets = Pets()
    filters = request.args.to_dict()
    data = []

    if not filters:
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
    """Obter detalhes de um pet.

    Busca um registro específico pelo seu ID único.
    
    O retorno inclui os dados detalhados do Cliente (Dono) associado.
    """
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
@pets_bp.arguments(CreatePetSchema, location="json") 
@pets_bp.response(201, GenericSuccessSchema, description="Pet cadastrado com sucesso")
@pets_bp.response(400, CreatePetResponseFailedSchema, description="Violação de regra de negócio")
@pets_bp.response(422, ValidationFailedSchema, description="Erro de validação (Campos obrigatórios ou formato inválido)")
@jwt_required()
def create_pet(pet_data): 
    """Cadastrar novo pet.

    Cria um novo registro no banco de dados.

    **Regras de Negócio:**
    * **Idade:** Deve ser enviada em **MESES** (ex: 2 anos = 24).
    * **Espécie:** Deve ser uma das opções válidas (Cachorro, Gato, etc).
    * **Sexo:** O sistema aceita 'm' ou 'f' e converte para maiúsculo automaticamente.
    """
    
    # Validação de Regra de Negócio (Sexo)
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
@pets_bp.arguments(UpdatePetSchema, location="json")
@pets_bp.response(200, GenericSuccessSchema, description="Atualização realizada")
@pets_bp.response(400, UpdatePetResponseFailedSchema, description="Erro na atualização")
@pets_bp.response(422, ValidationFailedSchema, description="Formato de dados inválido")
@jwt_required()
def update_pet(data, pet_id): 
    """Atualizar dados do pet.

    Atualiza parcialmente os dados. Envie apenas os campos que deseja alterar.
    
    * **Idade:** Se enviar, use meses.
    * **Imutável:** Não é possível alterar `id` ou `created_at`.
    """
    
    # Proteção extra contra alteração de ID/Data
    if "id" in data or "created_at" in data:
         return jsonify({
            "success": False,
            "point": "update_pet_validation",
            "message": "Não é permitido alterar id ou created_at manualmente"
        }), 422

    # Lógica de Sexo para Update
    if "sex" in data:
        sex = data.get("sex")
        if sex:
            if sex.upper() not in ('M', 'F'):
                return jsonify({
                    "success": False,
                    "point": "update_pet_validation",
                    "message": "O campo 'sex' deve ser 'M' (Macho) ou 'F' (Fêmea)."
                }), 400
            data["sex"] = sex.upper()

    pets = Pets()
    try:
        pets.update(pet_id, data)
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
    """Remover pet do sistema.

    Exclui permanentemente o registro.
    """
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