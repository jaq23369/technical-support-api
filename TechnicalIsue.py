
#Importamos Flask para crear la API Web
from flask import Flask, request, jsonify
# Importamos psycopg2 para conectarnos a PostgreSQL
import psycopg2
import psycopg2.extras
# Importamos datetime para manejar fechas
from datetime import datetime

# Creación de la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos PostgreSQL
DB_HOST = "localhost"
DB_NAME = "technical_support"  
DB_USER = "postgres"  
DB_PASS = "123456789"  
DB_PORT = "5432"  

# Función para conectar a la base de datos
def get_db_connection():
    # Creamos una conexión usando los parámetros definidos
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )
    # Activamos autocommit para que los cambios se guarden automáticamente
    conn.autocommit = True
    return conn

@app.route('/', methods=['GET'])
def get_welcome():
    return """
    <html>
        <head>
            <title>API Incidentes - Rutas</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 20px;
                }
                h1 {
                    color: #333;
                }
                ul {
                    list-style-type: none;
                    padding: 0;
                }
                li {
                    margin: 20px 0;
                }
                a {
                    text-decoration: none;
                    color: #007BFF;
                    font-weight: bold;
                }
                a:hover {
                    text-decoration: underline;
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                    background: #fff;
                    padding: 20px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    border-radius: 8px;
                }
                .description {
                    color: #555;
                    font-size: 14px;
                }
                code {
                    color: #d32baf;
                    font-family: Consolas, monospace;
                }
                pre {
                    background-color: #fafafa;
                    padding: 10px;
                    border-radius: 5px;
                    border: 1px solid #ddd;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>API de Incidentes - Rutas Disponibles</h1>
                <ul>
                    <li>
                        <a href="/incidents">GET /incidents</a>
                        <p class="description">
                            Obtiene la lista de todos los incidentes.<br>
                            <strong>Respuesta (JSON):</strong>
                        </p>
                        <pre>
[
  {
    "id": 1,
    "reporter": "Juan Pérez",
    "description": "La impresora no imprime en color.",
    "status": "pendiente",
    "created_at": "2025-03-28T12:00:00"
  },
  ...
]
                        </pre>
                    </li>

                    <li>
                        <a href="/incidents/1">GET /incidents/&lt;int:incident_id&gt;</a>
                        <p class="description">
                            Obtiene un incidente específico por su ID.<br>
                            <strong>Respuesta (JSON):</strong>
                        </p>
                        <pre>
{
  "id": 1,
  "reporter": "Juan Pérez",
  "description": "La impresora no imprime en color.",
  "status": "pendiente",
  "created_at": "2025-03-28T12:00:00"
}
                        </pre>
                    </li>

                    <li>
                        <strong>POST /incidents</strong>
                        <p class="description">
                            Crea un nuevo incidente.<br>
                            <strong>Cuerpo de la petición (JSON):</strong>
                        </p>
                        <pre>
{
  "reporter": "Carlos",
  "description": "La conexión es intermitente"
}
                        </pre>
                        <p class="description">
                            <strong>Respuesta (JSON):</strong> Incidente recién creado con su ID, status="pendiente" y created_at.
                        </p>
                        <pre>
{
  "id": 3,
  "reporter": "Carlos",
  "description": "La conexión es intermitente",
  "status": "pendiente",
  "created_at": "2025-03-28T13:00:00"
}
                        </pre>
                    </li>

                    <li>
                        <strong>PUT /incidents/&lt;int:incident_id&gt;</strong>
                        <p class="description">
                            Actualiza el estado de un incidente.<br>
                            <strong>Cuerpo de la petición (JSON):</strong>
                        </p>
                        <pre>
{
  "status": "en proceso"
}
                        </pre>
                        <p class="description">
                            <strong>Respuesta (JSON):</strong> El incidente actualizado.
                        </p>
                        <pre>
{
  "id": 1,
  "reporter": "Juan Pérez",
  "description": "La impresora no imprime en color.",
  "status": "en proceso",
  "created_at": "2025-03-28T12:00:00"
}
                        </pre>
                    </li>

                    <li>
                        <strong>DELETE /incidents/&lt;int:incident_id&gt;</strong>
                        <p class="description">
                            Elimina un incidente reportado por error.<br>
                            <strong>Respuesta:</strong> Código de estado <code>204 No Content</code> si la operación es exitosa.
                        </p>
                    </li>
                </ul>
            </div>
        </body>
    </html>
    """



# Endpoint para obtener un incidente específico por ID
@app.route('/incidents/<int:incident_id>', methods=['GET'])
def get_incident(incident_id):
    # Obtenemos una conexión a la base de datos
    conn = get_db_connection()
    # Creamos un cursor que devuelve resultados como diccionarios
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    # Ejecutamos la consulta SQL para obtener el incidente
    cur.execute("SELECT * FROM incidents WHERE id = %s", (incident_id,))
    incident = cur.fetchone()
    
    # Cerramos cursor y conexión
    cur.close()
    conn.close()
    
    if incident:
         # Convertimos la fecha a formato ISO para que sea JSON serializable
        incident['created_at'] = incident['created_at'].isoformat()
        return jsonify(incident)
    
     # Si no se encuentra el incidente, devolvemos error 404
    return jsonify({"error": "Incidente no encontrado"}), 404


# Endpoint para obtener todos los incidentes
@app.route('/incidents', methods=['GET'])
def get_incidents():
    # Obtenemos una conexión a la base de datos
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
     # Ejecutamos la consulta SQL para obtener todos los incidentes ordenados por ID
    cur.execute("SELECT * FROM incidents ORDER BY id")
    incidents = cur.fetchall()
    
    cur.close()
    conn.close()
    
    # Convertimos todas las fechas a formato ISO
    for incident in incidents:
        incident['created_at'] = incident['created_at'].isoformat()
    
    return jsonify(incidents)

# Crear incidentes en formato JSON
@app.route('/incidents', methods=['POST'])
def create_incident():
    # Convertimos todas las fechas a formato ISO
    data = request.json or {}

    # Validación 1: Verifica si existe el campo 'reporter'
    if not data.get("reporter"):
        return jsonify({"error": "El campo 'reporter' es obligatorio"}), 400

    # Validación 2: Verifica que la descripción tenga al menos 10 caracteres
    description = data.get("description", "")
    if len(description) < 10:
        return jsonify({"error": "La 'description' debe tener al menos 10 caracteres"}), 400

    # Establece conexión con la base de datos
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    # Inserta el nuevo incidente y retorna todos sus datos
    # RETURNING * devuelve el registro completo insertado
    cur.execute(
        "INSERT INTO incidents (reporter, description) VALUES (%s, %s) RETURNING *",
        (data["reporter"], data["description"])
    )
    
    # Obtiene el incidente recién creado
    new_incident = cur.fetchone()
    
    # Cierra las conexiones
    cur.close()
    conn.close()
    
    # Convierte la fecha a formato ISO para JSON
    new_incident['created_at'] = new_incident['created_at'].isoformat()
    
    # Retorna el nuevo incidente con código 201 (Created)
    return jsonify(new_incident), 201

# Actualizar el estado de un incidente
@app.route('/incidents/<int:incident_id>', methods=['PUT'])
def update_incident(incident_id):
    # Obtiene los datos JSON de la petición
    data = request.json or {}

    # Validación 1: Verifica que se incluya el campo 'status'
    if "status" not in data:
        return jsonify({"error": "El campo 'status' es requerido"}), 400

    # Validación 2: Verifica que el status sea válido
    valid_statuses = ["pendiente", "en proceso", "resuelto"]
    if data["status"] not in valid_statuses:
        return jsonify({"error": f"El estado debe ser uno de: {valid_statuses}"}), 400

    # Establece conexión con la base de datos
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    # Verifica si el incidente existe
    cur.execute("SELECT * FROM incidents WHERE id = %s", (incident_id,))
    incident = cur.fetchone()
    
    # Si no existe el incidente, retorna error 404
    if not incident:
        cur.close()
        conn.close()
        return jsonify({"error": "Incidente no encontrado"}), 404
    
    # Actualizar el estado del incidente
    cur.execute(
        "UPDATE incidents SET status = %s WHERE id = %s RETURNING *",
        (data["status"], incident_id)
    )
    
    updated_incident = cur.fetchone()
    
    # Cierra las conexiones
    cur.close()
    conn.close()
    
    ## Convierte la fecha a formato ISO para JSON
    updated_incident['created_at'] = updated_incident['created_at'].isoformat()
    
    # Retorna el nuevo incidente 
    return jsonify(updated_incident)

# Eliminar un incidente por ID
@app.route('/incidents/<int:incident_id>', methods=['DELETE'])
def delete_incident(incident_id):
    # Establecemos conexión con la base de datos
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Verificar si el incidente existe antes de eliminarlo
    cur.execute("SELECT id FROM incidents WHERE id = %s", (incident_id,))
    if cur.fetchone() is None:
         # Si no existe, cerramos conexiones y retornamos error 404
        cur.close()
        conn.close()
        return jsonify({"error": "Incidente no encontrado"}), 404
    
    # Si existe, se procede a eliminar el incidente
    cur.execute("DELETE FROM incidents WHERE id = %s", (incident_id,))
    
    # Cerramos las conexiones
    cur.close()
    conn.close()
    
    # Retornamos código 204 (No Content) indicando éxito sin contenido
    return '', 204


# Iniciamos la aplicación en modo debug en el puerto 5000.
if __name__ == '__main__':
    app.run(debug=True, port=5000)


