from ..utils.data_handler import DataHandler
from datetime import datetime as dt
from werkzeug.security import generate_password_hash

class Employees:
    def __init__(self):
        self.handler = DataHandler("employees")
    
    def list(self):
        data = self.handler.list_all()
        new_data = []
        for d in data:
            d.pop("password")
            new_data.append(d)
        return new_data
    
    def create(self, data: dict):
        self.handler.create({** data, "password": generate_password_hash(data.get("password")), "created_at": dt.now()})

    def delete(self, id):
        self.handler.delete(id)
    
    def update(self, id, data: dict):
        self.handler.update({**data, "id": id})

    def get_by_id(self, id):
        data = self.handler.get_by_id(id)
        data.pop("password")
        return data
    
    def search(self, filters: dict):
        filters_to_remove = ["logic", "operator"]
        data = self.handler.search({
            "logic": filters.get("logic", "AND"),
            "criteria": list(filter(lambda item: item.get("key", "") not in filters_to_remove,[{"key": key, "value": value, "operator": filters.get("operator", "CONTAINS")} for key,value in filters.items()]))
        })
        new_data = []
        for d in data:
            d.pop("password")
            new_data.append(d)
        return new_data