from marshmallow import Schema, fields, validate

VALID_SPECIES = ["Cachorro", "Gato", "Pássaro", "Peixe", "Roedor", "Outros"]
# --- SCHEMA BASE (Para exibição/GET) ---
class PetSchema(Schema):
    id = fields.String(
        required=True, 
        metadata={"description": "Identificador único do pet.", "example": "10"}
    )
    name = fields.String(
        required=True, 
        metadata={"description": "Nome completo do animal.", "example": "Thor"}
    )
    specie = fields.String(
        required=True, 
        metadata={"description": "Espécie do animal.", "example": "Cachorro"}
    )
    sex = fields.String(
        required=True, 
        metadata={"description": "Sexo biológico (M ou F).", "example": "M"}
    )
    age = fields.Integer(
        required=True, 
        metadata={"description": "Idade do animal em MESES.", "example": 24}
    )
    # owner_id como Dict porque o Service retorna o objeto Cliente completo
    owner_id = fields.Dict(
        required=True,
        metadata={
            "description": "Dados completos do dono do animal.",
            "example": {"id": 1, "name": "João Silva", "email": "joao@email.com"}
        }
    )
    created_at = fields.DateTime(
        format="%Y-%m-%d %H:%M:%S", 
        required=True,
        metadata={"description": "Data de registro.", "example": "2023-11-24 14:30:00"}
    )

# --- RESPOSTAS DE GET ---
class GetPetsResponseSchema(Schema):
    success = fields.Boolean(required=True, metadata={"example": True})
    data = fields.List(fields.Nested(PetSchema), required=True)

class GetPetsByIDResponseSchema(Schema):
    success = fields.Boolean(required=True, metadata={"example": True})
    data = fields.Nested(PetSchema, required=True)

class GetPetsByIDResponseNotFoundSchema(Schema):
    success = fields.Boolean(required=True, metadata={"example": False})
    point = fields.String(required=True, metadata={"example": "get_pet_by_id"})
    message = fields.String(required=True, metadata={"example": "Pet não encontrado"})

# --- CRIAÇÃO (POST) ---
class CreatePetSchema(Schema):
    name = fields.String(
        required=True, 
        metadata={"description": "Nome do pet.", "example": "Mel"}
    )
    specie = fields.String(
        required=True,
        validate=validate.OneOf(VALID_SPECIES), 
        metadata={
            "description": f"Espécie do animal. Opções: {', '.join(VALID_SPECIES)}.",
            "example": "Gato"
        }
    )
    sex = fields.String(
        required=True, 
        metadata={"description": "Sexo: 'M' (Macho) ou 'F' (Fêmea).", "example": "F"}
    )
    age = fields.Integer(
        required=True,
        # Garante que a idade não seja negativa
        validate=validate.Range(min=0, error="A idade deve ser maior ou igual a 0."),
        metadata={
            "description": "Idade do animal em MESES completos. (Ex: 2 anos = 24).",
            "example": 24
        }
    )
    # No cadastro, enviamos apenas o ID numérico
    owner_id = fields.Integer(
        required=True, 
        metadata={"description": "ID do cliente dono do pet.", "example": 1}
    )

class CreatePetResponseFailedSchema(Schema):
    success = fields.Boolean(required=True, metadata={"example": False})
    point = fields.String(required=True, metadata={"example": "create_pet"})
    message = fields.String(required=True, metadata={"example": "Dados inválidos"})

# --- ATUALIZAÇÃO (PATCH) ---
class UpdatePetSchema(Schema):
    name = fields.String(required=False, metadata={"example": "Mel da Silva"})
    specie = fields.String(
        required=False,
        validate=validate.OneOf(VALID_SPECIES), 
        metadata={"example": "Gato"}
    )
    sex = fields.String(required=False, metadata={"description": "M ou F", "example": "F"})
    age = fields.Integer(
        required=False, 
        validate=validate.Range(min=0),
        metadata={"description": "Idade em meses", "example": 25}
    )

class UpdatePetResponseFailedSchema(Schema):
    success = fields.Boolean(required=True, metadata={"example": False})
    point = fields.String(required=True, metadata={"example": "update_pet"})
    message = fields.String(required=True, metadata={"example": "Erro na atualização"})

# --- DELEÇÃO ---
class DeletePetResponseFailedSchema(Schema):
    success = fields.Boolean(required=True, metadata={"example": False})
    point = fields.String(required=True, metadata={"example": "delete_pet"})
    message = fields.String(required=True, metadata={"example": "Pet não encontrado"})