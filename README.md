API de Soporte Técnico

Para crear este esqueleto de la API de soporte tecnico se utilizo python con Flask y para la base de datos se utilizará pgAdmin4 (PostgresSQL)


Este proyecto es una API REST sencilla que permite a los empleados de la empresa reportar incidentes relacionados con sus equipos de trabajo (computadoras, impresoras, redes, etc.). Está desarrollada con Flask y, por el momento, guarda la información en memoria sin persistirla en una base de datos.

Características:

1.Crear reportes de incidentes (POST).

2.Listar todos los incidentes (GET).
El objetivo de este proyecto es servir como base para una solución de soporte técnico, permitiendo la futura integración con bases de datos y ampliaciones de funcionalidad.

Requisitos:

-Python 3.7+
-Flask (instalable vía pip)
-Otras dependencias que desees incluir (por ejemplo, datetime ya viene en la biblioteca estándar de Python)


Uso de la API:

Endpoints
-GET /
Devuelve un mensaje de bienvenida y describe los endpoints.
Ejemplo: http://127.0.0.1:5000/

-GET /incidents
Obtiene la lista de todos los incidentes reportados.
Ejemplo: http://127.0.0.1:3001/incidents

-POST /incidents
Crea un nuevo incidente.
Campos requeridos:
reporter (obligatorio)
description (al menos 10 caracteres)

El incidente se crea con status="pendiente" y se registra la fecha/hora de creación en created_at.


Funcionamiento Interno:

El proyecto usa:

Python y Flask para levantar un servidor web rápido y sencillo.
Un arreglo en memoria (incidents) como almacenamiento temporal. Los datos se pierden al reiniciar la aplicación.

Validaciones mínimas:
-reporter debe existir.
-description debe tener 10 o más caracteres.

Al crear un incidente, se le asigna un id incrementado con base a la longitud de la lista existente, y se establece su status inicial como "pendiente".





