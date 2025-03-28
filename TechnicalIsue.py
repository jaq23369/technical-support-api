
#Este archivo define una API sencilla en Flask para manejar incidentes de soporte.
#Se implementan los métodos GET (lista de incidentes) y POST (crear un incidente),
#manteniendo los datos en una lista en memoria.

from flask import Flask, request, jsonify
from datetime import datetime

# Creación de la aplicación Flask
app = Flask(__name__)

# Base de datos simulada en la memoria donde cada incidiente corresponde a un diccionario
incidents = [
    {
        "id": 1,
        "reporter": "Juan Pérez",
        "description": "La impresora no imprime en color.",
        "status": "pendiente",
        "created_at": datetime.utcnow().isoformat()
    },
    {
        "id": 2,
        "reporter": "María López",
        "description": "La conexión a internet es muy lenta.",
        "status": "pendiente",
        "created_at": datetime.utcnow().isoformat()
    }
]

#Endpoint raíz de la aplicación que muestra una bienvenida y la lista de endpoints disponibles
@app.route('/', methods=['GET'])
def get_welcome():
    return jsonify({
        "message": "Bienvenido a la API de Incidentes",
        "endpoints": {
            "GET /incidents": "Obtener la lista de incidentes",
            "GET /incidents/<int:incident_id>": "Obtener un incidente específico",
            "POST /incidents": "Crear un nuevo incidente"
        }
    })

# Obtener incidentes en formato JSON
@app.route('/incidents', methods=['GET'])
def get_incidents():
    return jsonify(incidents)

# Crear incidentes en formato JSON
# Si no encuentra JSON, usa un diccionario vacío para evitar errores.
@app.route('/incidents', methods=['POST'])
def create_incident():
    data = request.json or {}

    # Validación: 'reporter' es un campo obligatorio.
    if not data.get("reporter"):
        return jsonify({"error": "El campo 'reporter' es obligatorio"}), 400

   # Validación: 'description' debe existir y tener al menos 10 caracteres.
    description = data.get("description", "")
    if len(description) < 10:
        return jsonify({"error": "La 'description' debe tener al menos 10 caracteres"}), 400

    # Creación de un nuevo incidente
    new_id = len(incidents) + 1
    new_incident = {
        "id": new_id,
        "reporter": data["reporter"],
        "description": data["description"],
        "status": "pendiente",  # por defecto se inicia en "pendiente"
        "created_at": datetime.utcnow().isoformat()
    }

    # Agregamos el nuevo incidente a la lista.  
    incidents.append(new_incident)

    # Retornamos el incidente creado junto con un código de estado 201 (Created).
    return jsonify(new_incident), 201

# Iniciamos la aplicación en modo debug en el puerto 5000.
if __name__ == '__main__':
    app.run(debug=True, port=5000)

