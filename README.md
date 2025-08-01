Task Manager API

Sistema de gestión de tareas colaborativo: backend desarrollado en Python (Flask), PostgreSQL y seguridad JWT, todo dockerizado y preparado para desarrollo ágil. Compatible con equipos y listo para ampliaciones.
Características

    API REST para gestión de tareas con campos flexibles.

    Manejo de usuarios y autenticación segura (JWT).

    Tabla de estados de tareas modificable.

    CRUD completo: crear, editar, eliminar y listar tareas (con filtros).

    Seguridad por roles (admin, usuario).

    Arquitectura escalable, portable con Docker.

    Preparado para integración continua y despliegue fácil.

Requisitos

    Docker y Docker Compose instalados

    Git

Instalación y despliegue rápido

    Clona el repositorio:

bash
git clone https://github.com/tu_usuario/task_manager.git
cd task_manager

Levanta los contenedores:

    bash
    docker-compose up --build

La aplicación Flask quedará corriendo en:
http://localhost:5000/api/

La base de datos PostgreSQL estará disponible en el servicio Docker llamado db.
Primeros pasos
1. Crea usuarios y estados iniciales

    Usa los scripts de inicialización (crea_user.py, crea_estados.py) o crea usuarios/estados por consola de Python siguiendo el manual o utilizando las rutas del API.

2. Autenticación

Obtén tu token JWT haciendo login:

bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"usuario":"admin", "clave":"adminpass"}' \
  http://localhost:5000/api/auth/login

Resguarda tu token para todas las peticiones protegidas.
3. Rutas principales del API
Método	Endpoint	Descripción	Autenticación
POST	/api/auth/login	Login y obtención de token	No
POST	/api/tasks/	Crear nueva tarea	Sí (JWT)
GET	/api/tasks/	Listar todas las tareas	Sí (JWT)
GET	/api/tasks/?estado=nombre_estado	Listar tareas filtradas por estado	Sí (JWT)
PUT	/api/tasks/<id>	Modificar tarea existente	Sí (JWT)
DELETE	/api/tasks/<id>	Eliminar tarea	Sí (JWT)
GET	/api/tasks/estados/	Listar todos los estados de tarea	Sí (JWT)
POST	/api/tasks/estados/	Crear un nuevo estado (solo admin)	Sí (JWT, perfil admin)

Nota: Todos los endpoints excepto /login requieren header:
Authorization: Bearer <TOKEN>
Ejemplos de consumo con curl
Crear tarea

bash
curl -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name":"Mi tarea","description":"Detalle","due_date":"2025-08-05","estado":"pendiente"}' \
  http://localhost:5000/api/tasks/

Editar tarea

bash
curl -X PUT -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"estado":"Terminado", "description":"Finalizada"}' \
  http://localhost:5000/api/tasks/1

Eliminar tarea

bash
curl -X DELETE -H "Authorization: Bearer $TOKEN" \
  http://localhost:5000/api/tasks/1

Variables de entorno relevantes

    El acceso a la base usa:

        postgres:postgres@db:5432/taskdb

    Cambia SECRET_KEY en /app/__init__.py para mayor seguridad.

Estructura del proyecto

text
.
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── run.py
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── database.py
│   ├── models.py
│   └── routes.py

Pruebas

Puedes agregar tests en el directorio /tests usando frameworks como pytest o unittest. Para correr los tests, ejecuta los scripts desde el contenedor app (crea tus archivos de prueba como test_app.py).
Contribuciones

    Crea un fork y pull request detallando tus cambios.

    Sigue la convención de mensajes de commit y documenta nuevas endpoints o cambios en README.

Licencia

MIT (o la de tu elección).

¡Este README te servirá como manual básico para tu equipo y para cualquier persona que use o colabore con tu repositorio en GitHub!
Puedes editar cualquier sección y agregar instrucciones más avanzadas si implementas nuevas funciones.
