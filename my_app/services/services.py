from ..utils.data_handler import DataHandler
from datetime import datetime as dt

class Services:
    def __init__(self):
        self.handler = DataHandler("services")
    
    def list(self):
        data = self.handler.list_all()
        return data
    
    def create(self, data: dict):
        self.handler.create({** data, "created_at": dt.now()})

    def delete(self, id):
        self.handler.delete(id)
    
    def update(self, id, data: dict):
        self.handler.update({**data, "id": id})

    def get_by_id(self, id):
        return self.handler.get_by_id(id)
    
    def search(self, filters: dict):
        filters_to_remove = ["logic", "operator"]
        return self.handler.search({
            "logic": filters.get("logic", "AND"),
            "criteria": list(filter(lambda item: item.get("key", "") not in filters_to_remove,[{"key": key, "value": value, "operator": filters.get("operator", "CONTAINS")} for key,value in filters.items()]))
        })