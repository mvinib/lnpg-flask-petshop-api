from marshmallow import Schema, fields

# -----------------------------------------------------------------------------
# SCHEMA PRINCIPAL
# -----------------------------------------------------------------------------
class ServiceSchema(Schema):
    id = fields.String(dump_only=True, metadata={"description": "ID do serviço", "example": "1"})
    name = fields.String(required=True, metadata={"description": "Nome do serviço", "example": "Banho e Tosa"})
    description = fields.String(required=True, metadata={"description": "Detalhes do serviço", "example": "Completo com corte de unhas"})
    value = fields.Float(required=True, metadata={"description": "Preço do serviço", "example": 80.00})
    created_at = fields.DateTime(format="%Y-%m-%d %H:%M:%S.%f", dump_only=True)

# -----------------------------------------------------------------------------
# SCHEMAS DE RESPOSTA
# -----------------------------------------------------------------------------
class GetServicesResponseSchema(Schema):
    success = fields.Boolean(required=True, metadata={"example": True})
    data = fields.List(
        fields.Nested(ServiceSchema), 
        required=True,
        metadata={"description": "Lista de serviços disponíveis"}
    )

class GetServiceByIDResponseSchema(Schema):
    success = fields.Boolean(required=True, metadata={"example": True})
    data = fields.Nested(
        ServiceSchema, 
        required=True,
        metadata={"description": "Dados do serviço encontrado"}
    )

class GetServiceByIDResponseNotFoundSchema(Schema):
    success = fields.Boolean(required=True, metadata={"example": False})
    point = fields.String(required=True, metadata={"example": "get_service_by_id"})
    message = fields.String(required=True, metadata={"example": "Serviço não encontrado"})

# -----------------------------------------------------------------------------
# SCHEMAS DE ENTRADA
# -----------------------------------------------------------------------------
class CreateServiceSchema(Schema):
    name = fields.String(required=True, metadata={"description": "Nome do serviço", "example": "Vacina V10"})
    description = fields.String(required=True, metadata={"description": "Descrição detalhada", "example": "Vacina anual importada"})
    value = fields.Float(required=True, metadata={"description": "Valor em reais", "example": 120.00})

class UpdateServiceSchema(Schema):
    name = fields.String(required=False, metadata={"example": "Vacina V8"})
    description = fields.String(required=False, metadata={"example": "Vacina nacional"})
    value = fields.Float(required=False, metadata={"example": 100.00})

# -----------------------------------------------------------------------------
# SCHEMAS DE ERRO
# -----------------------------------------------------------------------------
class CreateServiceResponseFailedSchema(Schema):
    success = fields.Boolean(required=True, metadata={"example": False})
    point = fields.String(required=True, metadata={"example": "create_service"})
    message = fields.String(required=True, metadata={"example": "Erro ao criar serviço"})

class DeleteServiceResponseFailedSchema(Schema):
    success = fields.Boolean(required=True, metadata={"example": False})
    point = fields.String(required=True, metadata={"example": "delete_service"})
    message = fields.String(required=True, metadata={"example": "ID não existe"})

class UpdateServiceResponseFailedSchema(Schema):
    success = fields.Boolean(required=True, metadata={"example": False})
    point = fields.String(required=True, metadata={"example": "update_service"})
    message = fields.String(required=True, metadata={"example": "ID não existe"})