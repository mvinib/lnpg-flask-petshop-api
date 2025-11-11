import os
from my_app import create_app
from my_app.data_handler import DataHandler 
from datetime import datetime as dt

app = create_app()

with app.app_context():
    handler = DataHandler("pets")
    try:
        handler.create([2, "Biruta", "cat", "felina", "2", 90, dt.now()])
    except Exception as err: 
        print(err)
    
    dados = handler.search(filters={
        "logic": "AND",
        "criteria": [
            {
                "key": "name",
                "operator": "CONTAINS",
                "value": "Ab"
            },
        ]
    })

    print("Dados encontrados:")
    print(dados)
    print("------------------------------")

if __name__ == '__main__':
    app.run()