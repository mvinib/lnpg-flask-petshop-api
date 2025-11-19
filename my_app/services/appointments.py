from ..utils.data_handler import DataHandler
from ..utils.validate import validateScheduledAt
from datetime import datetime as dt, date
from .pets import Pets
from .services import Services
from .employees import Employees
from typing import List, Dict, Any

class Appointments:
    def __init__(self):
        self.handler = DataHandler("appointments")
    
    def list(self):
        data = self.handler.list_all()
        return self.get_relationship(data)
    
    def create(self, data: dict):
        pets = Pets()
        services = Services()
        employees = Employees()

        if not pets.get_by_id(data.get("pet_id")):
            raise Exception("Pet não encontrado")
        
        if not services.get_by_id(data.get("service_id")):
            raise Exception("Serviço não encontrado")
        
        if not employees.get_by_id(data.get("employee_id")):
            raise Exception("Funcionário não encontrado")

        if not validateScheduledAt(data.get("scheduled_at")):
            raise Exception("Informe uma data válida")
        
        self.handler.create({** data, "created_at": dt.now() , "status": "scheduled"})

    def delete(self, id):
        self.handler.delete(id)
    
    def update(self, id, data: dict):
        pets = Pets()
        services = Services()
        employees = Employees()

        pet_id = data.get("pet_id", None)
        service_id = data.get("service_id", None)
        employee_id = data.get("employee_id", None)
        scheduled_at = data.get("scheduled_at", None)
        
        if pet_id and not pets.get_by_id(pet_id):
            raise Exception("Pet não encontrado")
        
        if service_id and not services.get_by_id(service_id):
            raise Exception("Serviço não encontrado")
        
        if employee_id and not employees.get_by_id(employee_id):
            raise Exception("Funcionário não encontrado")

        if scheduled_at and not validateScheduledAt(scheduled_at):
            raise Exception("Informe uma data válida")
        
        self.handler.update({**data, "id": id})

    def get_by_id(self, id):
        appointment = self.handler.get_by_id(id)
        if appointment:
            return self.get_relationship([appointment])[0]
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
        services = Services()
        employees = Employees()

        for index, value in enumerate(list):
            pet_id = value.pop("pet_id")
            service_id = value.pop("service_id")
            employee_id = value.pop("employee_id")

            pet = pets.get_by_id(pet_id)
            service = services.get_by_id(service_id)
            employee = employees.get_by_id(employee_id)

            list[index] = {
                **value,
                "pet": pet,
                "service": service,
                "employee": employee
            }

        return list
