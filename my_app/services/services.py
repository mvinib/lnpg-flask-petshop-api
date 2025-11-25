from ..utils.data_handler import DataHandler
from datetime import datetime as dt

class Services:
    def __init__(self):
        self.handler = DataHandler("services")
    
    def list(self):
        return self.handler.list_all()
    
    def create(self, data: dict):
        # Adiciona a data de criação automaticamente
        self.handler.create({**data, "created_at": dt.now()})

    def delete(self, id):
        self.handler.delete(id)
    
    def update(self, id, data: dict):
        self.handler.update({**data, "id": id})

    def get_by_id(self, id):
        return self.handler.get_by_id(id)
    
    def search(self, filters: dict):
        # Lista de chaves que NÃO são colunas do CSV, mas comandos de busca
        filters_to_remove = ["logic", "operator"]
        
        # Monta a estrutura complexa de critérios que o DataHandler espera
        return self.handler.search({
            "logic": filters.get("logic", "AND"),
            "criteria": list(filter(
                lambda item: item.get("key", "") not in filters_to_remove,
                [
                    {
                        "key": key, 
                        "value": value, 
                        "operator": filters.get("operator", "CONTAINS")
                    } 
                    for key, value in filters.items()
                ]
            ))
        })