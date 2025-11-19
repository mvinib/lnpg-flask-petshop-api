from ..utils.data_handler import DataHandler
from datetime import datetime as dt
from typing import List, Dict, Any
from .pets import Pets

class Clients:
    def __init__(self):
        self.handler = DataHandler("clients")
    
    def list(self):
        data = self.handler.list_all()
        return self.get_relationship(data)
    
    def create(self, data: dict):
        email_alreadys_exist = self.search({
            "email": data.get("email")
        })

        if email_alreadys_exist:
            raise Exception("O e-mail informado já está em uso")
        
        self.handler.create({** data, "created_at": dt.now()})

    def delete(self, id):
        self.handler.delete(id)
    
    def update(self, id, data: dict):
        self.handler.update({**data, "id": id})

    def get_by_id(self, id):
        client = self.handler.get_by_id(id)
        if client:
            return self.get_relationship([client])[0]
        return None
    
    def search(self, filters: dict):
        filters_to_remove = ["logic", "operator"]
        data = self.handler.search({
            "logic": filters.get("logic", "AND"),
            "criteria": list(filter(lambda item: item.get("key", "") not in filters_to_remove,[{"key": key, "value": value, "operator": filters.get("operator", "CONTAINS")} for key,value in filters.items()]))
        })
        return self.get_relationship(data)

    def get_relationship(self, list: List[Dict[str, Any]]):
        pets = Pets()

        for index, value in enumerate(list):
            list_pets = pets.search({
                "owner_id": value.get("id"),
                "operator": "EQUAL"
            })

            list[index] = {
                **value,
                "pets": list_pets
            }

        return list