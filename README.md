API de Soporte Técnico

Este proyecto implementa una API para gestionar incidentes de soporte técnico. La API permite a los empleados reportar incidentes relacionados con equipos de trabajo como computadoras, impresoras, redes, etc. Los incidentes se almacenan en una base de datos PostgreSQL.

-------------------------------------------------------------------------------------------------------

Requisitos

Python 3.7+
PostgreSQL 14 o superior

-------------------------------------------------------------------------------------------------------

Instalación y Configuración

Instalar Python 3 (si no se tiene instalado)
macOS suele venir con Python 2.x instalado. Recuerda revisar tu versión con:
python3 --version

Si no se tiene o es muy antiguo, se recomienda descargar la versión más reciente de Python o instálarlo con Homebrew:
brew install python

Instalar PostgreSQL con Homebrew
Instala PostgreSQL (versión 14 en este ejemplo):
brew install postgresql@14

(Opcional) Verifica la instalación:
psql --version
Debería mostrar algo como: psql (PostgreSQL) 14.x

Instalar Flask y psycopg2 en macOS (rompiendo restricciones)
En algunos entornos de macOS gestionados por Homebrew, al ejecutar pip3 install ..., puedes obtener un error de tipo “externally-managed-environment”. Para solucionarlo, se puede usar la bandera --break-system-packages, asumiendo que comprendes los riesgos:

Instalar Flask:
pip3 install flask --break-system-packages

Instalar psycopg2:
pip3 install psycopg2 --break-system-packages

-------------------------------------------------------------------------------------------------------

Explicación de la Base de Datos:
La base de datos fue creada en pgAdmin4 (PostgresSQL) de la siguiente forma:

CREATE DATABASE technical_support;

CREATE TABLE incidents (
    id SERIAL PRIMARY KEY,
    reporter VARCHAR(100),
    description TEXT,
    status VARCHAR(20) DEFAULT 'pendiente',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Y se le hicieron 20 inserts que son los siguiente:

INSERT INTO incidents (reporter, description, status) VALUES 
('Juan Pérez', 'La impresora no imprime en color.', 'pendiente'),
('María López', 'La conexión a internet es muy lenta.', 'pendiente'),
('Carlos Gómez', 'El sistema no responde al intentar abrir aplicaciones.', 'pendiente'),
('Ana Martínez', 'El teclado no responde al presionar algunas teclas.', 'pendiente'),
('Luis Fernández', 'La pantalla de la computadora está parpadeando.', 'pendiente'),
('Ricardo Sánchez', 'No puedo acceder a la red Wi-Fi.', 'pendiente'),
('Laura Torres', 'El software de contabilidad se cierra inesperadamente.', 'pendiente'),
('Pedro Ramírez', 'El monitor no se enciende.', 'pendiente'),
('Julia Rodríguez', 'La impresora se atasca con frecuencia.', 'pendiente'),
('Oscar García', 'El sonido no funciona en el equipo.', 'pendiente'),
('Patricia Pérez', 'El sistema se congela al intentar abrir archivos grandes.', 'pendiente'),
('Eduardo Díaz', 'No puedo acceder a la red interna de la empresa.', 'pendiente'),
('Susana Jiménez', 'El mouse no se mueve correctamente.', 'pendiente'),
('Mario Delgado', 'La computadora se reinicia por sí sola.', 'pendiente'),
('Carolina Ruiz', 'La luz del teclado está apagada.', 'pendiente'),
('Javier Mendoza', 'El software de video no reproduce archivos multimedia.', 'pendiente'),
('Teresa Gómez', 'El servidor de archivos está caído.', 'pendiente'),
('Fernando García', 'El monitor tiene líneas horizontales.', 'pendiente'),
('Isabel López', 'El sistema se congela al intentar realizar una actualización.', 'pendiente'),
('Carlos Martínez', 'No puedo acceder al servidor de correo electrónico.', 'pendiente');

Para ver cambios en la base de datos utilizar el siguiente comando en pgAdmin4
SELECT * FROM incidents;

-------------------------------------------------------------------------------------------------------

Ejecución de la API

Asegurarse de que PostgreSQL esté corriendo:
brew services start postgresql@14

Iniciar la aplicación Flask:
flask --app TechnicalIsue run --debug

La API estará disponible en http://127.0.0.1:5000

Cuando se termine de probar la API parar el PostgreSQL con el siguiente comando:
brew services stop postgresql@14

-------------------------------------------------------------------------------------------------------

Probar la API

Recomiendo usar Postman:

@app.route('/incidents', methods=['GET'])
def get_incidents():
   
    Obtiene todos los incidentes.

    # 1. Conexión a la base de datos
    conn = get_db_connection()

    # 2. Cursor que devuelve filas como diccionarios
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # 3. Ejecuta la consulta para obtener todos los incidentes
    cur.execute("SELECT * FROM incidents ORDER BY id")
    incidents = cur.fetchall()

    # 4. Cerrar cursor y conexión
    cur.close()
    conn.close()

    # 5. Convertir 'created_at' a formato ISO para cada incidente
    for incident in incidents:
        incident['created_at'] = incident['created_at'].isoformat()

    # 6. Devolver en formato JSON
    return jsonify(incidents)
    
-------------------------------------------------------------------------------------------------------

@app.route('/incidents/<int:incident_id>', methods=['GET'])
def get_incident(incident_id):
    
    Obtiene un incidente por ID.
   
    # 1. Conexión a la base de datos
    conn = get_db_connection()

    # 2. Cursor que devuelve filas como diccionarios
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    # 3. Ejecuta la consulta parametrizada
    cur.execute("SELECT * FROM incidents WHERE id = %s", (incident_id,))
    incident = cur.fetchone()

    # 4. Cerrar cursor y conexión
    cur.close()
    conn.close()

    # 5. Si el incidente existe, convertir 'created_at' a ISO y retornar JSON
    if incident:
        incident['created_at'] = incident['created_at'].isoformat()
        return jsonify(incident)

    # 6. Si no existe, retornar 404
    return jsonify({"error": "Incidente no encontrado"}), 404

-------------------------------------------------------------------------------------------------------

@app.route('/incidents', methods=['POST'])
def create_incident():
    
    Crea un nuevo incidente.
    
    # 1. Leer el JSON del body
    data = request.json or {}

    # 2. Validaciones: reporter es obligatorio, description >= 10 caracteres
    if not data.get("reporter"):
        return jsonify({"error": "El campo 'reporter' es obligatorio"}), 400

    if not data.get("description") or len(data["description"]) < 10:
        return jsonify({"error": "La 'description' debe tener al menos 10 caracteres"}), 400

    # 3. Conexión y cursor
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    # 4. Insertar el incidente (status por defecto = 'pendiente')
    cur.execute(
        "INSERT INTO incidents (reporter, description) VALUES (%s, %s) RETURNING *",
        (data["reporter"], data["description"])
    )
    new_incident = cur.fetchone()

    # 5. Cerrar cursor y conexión
    cur.close()
    conn.close()

    # 6. Convertir 'created_at' a ISO y retornar en JSON
    new_incident['created_at'] = new_incident['created_at'].isoformat()
    return jsonify(new_incident), 201


-------------------------------------------------------------------------------------------------------

@app.route('/incidents/<int:incident_id>', methods=['PUT'])
def update_incident(incident_id):
    
    Actualiza el status de un incidente.
    
    # 1. Leer el JSON
    data = request.json or {}

    # 2. Validar que 'status' venga en el body
    if "status" not in data:
        return jsonify({"error": "El campo 'status' es requerido"}), 400

    # 3. Validar que 'status' sea uno de los valores permitidos
    valid_statuses = ["pendiente", "en proceso", "resuelto"]
    if data["status"] not in valid_statuses:
        return jsonify({"error": f"El estado debe ser uno de {valid_statuses}"}), 400

    # 4. Conexión y cursor
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # 5. Verificar si el incidente existe
    cur.execute("SELECT * FROM incidents WHERE id = %s", (incident_id,))
    incident = cur.fetchone()

    if not incident:
        cur.close()
        conn.close()
        return jsonify({"error": "Incidente no encontrado"}), 404

    # 6. Actualizar el incidente
    cur.execute(
        "UPDATE incidents SET status = %s WHERE id = %s RETURNING *",
        (data["status"], incident_id)
    )
    updated_incident = cur.fetchone()

    # 7. Cerrar cursor y conexión
    cur.close()
    conn.close()

    # 8. Convertir 'created_at' a ISO y devolver
    updated_incident['created_at'] = updated_incident['created_at'].isoformat()
    return jsonify(updated_incident)


-------------------------------------------------------------------------------------------------------

@app.route('/incidents/<int:incident_id>', methods=['DELETE'])
def delete_incident(incident_id):
    
    Elimina un incidente específico por ID.
    
    # 1. Conexión y cursor
    conn = get_db_connection()
    cur = conn.cursor()

    # 2. Verificar si el incidente existe
    cur.execute("SELECT id FROM incidents WHERE id = %s", (incident_id,))
    if cur.fetchone() is None:
        cur.close()
        conn.close()
        return jsonify({"error": "Incidente no encontrado"}), 404

    # 3. Eliminarlo
    cur.execute("DELETE FROM incidents WHERE id = %s", (incident_id,))

    # 4. Cerrar
    cur.close()
    conn.close()

    # 5. Respuesta: 204 No Content
    return '', 204


-------------------------------------------------------------------------------------------------------

Docker

Prerrequisitos:
-Docker Desktop (Siempre tenerlo abierto para que funcionen los comandos)

Levantar la API con Docker:

# 1. Clonar el repositorio
git clone https://github.com/jaq23369/technical-support-api.git

# 2. Acceder a la carpeta donde clonaste el repositorio desde VScode

# 3. Construir, levantar y detener los contenedores
Primero ejecutar: docker-compose up --build
Segundo: Luego de que se contruya el docker verás este mensaje: Accede a la aplicación en http://localhost:5001, aquí es donde puedes probar la API
Tercero: Una vez probadad la API regresa a VScode y ejecuta el comando CRTL + C para detener los contenedores
Cuarto: Ejecuta este comando: docker-compose down para detenerlo definitivamente.

------------------------------------------------------------------------------------------------------

Descripción de archivos de configuración

------------------------------------------------------------------------------------------------------

docker-compose.yml:

Servicios:

app: Aplicación Flask.

db: Base de datos PostgreSQL.

build: . construye la imagen usando el Dockerfile en la raíz.

ports: "5001:5001" expone el puerto 5001 del contenedor en el host.

environment: variables de conexión a PostgreSQL (DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT).

depends_on: arranca primero el servicio db.

volumes:

./static:/app/static y ./templates:/app/templates para recarga de archivos estáticos en caliente.

restart: always reinicia el contenedor app si falla.

------------------------------------------------------------------------------------------------------

El servicio db:

image: postgres:13 usa PostgreSQL v13.

environment: define POSTGRES_DB, POSTGRES_USER y POSTGRES_PASSWORD.

volumes:

postgres_data persiste datos en un volumen Docker.

./init.sql se ejecuta al iniciar para poblar la tabla incidents.

ports: "5434:5433" mapea internamente el puerto 5433 al 5434 en el host.

------------------------------------------------------------------------------------------------------

Dockerfile:

Base: python:3.9-slim para una imagen ligera.

ENV PYTHONDONTWRITEBYTECODE=1: evita archivos .pyc.

ENV PYTHONUNBUFFERED=1: no bufferiza la salida.

Usuario: crea appuser (UID 10001) para mayor seguridad.

Dependencias: instala según requirements.txt con caché de pip.

Directorios: crea static y templates y cede permisos al usuario.

Copia el código al contenedor y ajusta permisos.

USER appuser: no se ejecuta como root.

EXPOSE 5001: puerto que escucha Flask.

CMD ["python", "TechnicalIsue.py"]: comando de arranque.

------------------------------------------------------------------------------------------------------

init.sql:

Script SQL que monta la base de datos al arrancar.

Crea la tabla incidents con campos id, reporter, description, status, created_at.

Inserta 20 registros de ejemplo para pruebas.

------------------------------------------------------------------------------------------------------

requirements.txt:

Lista de librerías Python necesarias:

Flask==2.0.1: microframework web.

Werkzeug==2.0.3: servidor WSGI.

psycopg2-binary==2.9.1: driver PostgreSQL.

------------------------------------------------------------------------------------------------------