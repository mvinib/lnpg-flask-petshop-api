from typing import List, AnyStr
from flask import jsonify
from datetime import datetime as dt, date

def schemaValidate(list_fields: List[AnyStr], data: dict, missing = True):
    if missing:
        missing_fields = []
        for field in list_fields:
            if field not in data or not data[field]:
                missing_fields.append(field)
                
        if missing_fields:
            return jsonify({
                "success": False,
                "error": "Campos obrigatórios estão faltando ou estão vazios.",
                "missing": missing_fields
            }), 422 

        return None
    else:
        blocked_fields = []
        for field in list_fields:
            if field in data:
                blocked_fields.append(field)
                
        if blocked_fields:
            return jsonify({
                "success": False,
                "error": "Alguns campos informados estão bloqueados.",
                "blocked": blocked_fields
            }), 422 

        return None
    

def validateScheduledAt(date_string: str, date_format='%Y-%m-%dT%H:%M:%S.%f'):
        if not date_string:
            return False 
        
        actual_date = date.today()

        try:
            scheduled_dt = dt.strptime(date_string, date_format)
            scheduled_date = scheduled_dt.date()

            return scheduled_date >= actual_date
        except ValueError:
            return False
   
