from flask import Blueprint, request, jsonify
from .models import Task, Usuario, EstadoTarea
from .database import db
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from .auth import token_required

task_bp = Blueprint('tasks', __name__)

def parse_date(text):
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None

@task_bp.route('/estados/', methods=['GET'])
@token_required
def list_estados():
    estados = EstadoTarea.query.all()
    return jsonify([{'id': e.id, 'nombre': e.nombre} for e in estados]), 200

@task_bp.route('/estados/', methods=['POST'])
@token_required
def create_estado():
    if request.perfil != 'admin':
        return jsonify({'error': 'Solo administradores pueden crear estados'}), 403
    data = request.json
    nombre = data.get('nombre', '').strip()
    if not nombre:
        return jsonify({'error': 'El nombre es obligatorio'}), 400
    if EstadoTarea.query.filter_by(nombre=nombre).first():
        return jsonify({'error': 'El estado ya existe'}), 409
    estado = EstadoTarea(nombre=nombre)
    db.session.add(estado)
    db.session.commit()
    return jsonify({'id': estado.id, 'nombre': estado.nombre}), 201

@task_bp.route('/', methods=['GET'])
@token_required
def list_tasks():
    estado_nombre = request.args.get('estado')
    query = Task.query
    if estado_nombre:
        estado = EstadoTarea.query.filter_by(nombre=estado_nombre).first()
        if not estado:
            return jsonify([]), 200
        query = query.filter_by(estado_id=estado.id)
    tasks = query.all()
    result = []
    for t in tasks:
        result.append({
            'id': t.id,
            'name': t.name,
            'description': t.description,
            'due_date': t.due_date.isoformat() if t.due_date else None,
            'estado': t.estado.nombre if t.estado else None,
            'usuario': t.usuario.nombre_completo if t.usuario else None,
            'created_at': t.created_at.isoformat(),
            'updated_at': t.updated_at.isoformat()
        })
    return jsonify(result), 200

@task_bp.route('/', methods=['POST'])
@token_required
def create_task():
    data = request.json or {}
    name = data.get('name', '').strip()
    description = data.get('description', '')
    due_date = parse_date(data.get('due_date'))
    estado_nombre = data.get('estado', 'pendiente')

    if not name:
        return jsonify({'error': 'El nombre de la tarea es obligatorio.'}), 400
    estado = EstadoTarea.query.filter_by(nombre=estado_nombre).first()
    if not estado:
        return jsonify({'error': f"Estado '{estado_nombre}' no existe"}), 400

    task = Task(
        name=name,
        description=description,
        due_date=due_date,
        estado_id=estado.id,
        usuario_id=request.user_id
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({'message': "Tarea creada", 'id': task.id}), 201

@task_bp.route('/<int:id>', methods=['PUT'])
@token_required
def edit_task(id):
    task = Task.query.get_or_404(id)
    data = request.json or {}

    if 'name' in data:
        new_name = data['name'].strip()
        if not new_name:
            return jsonify({"error": "El nombre no puede estar vacío."}), 400
        task.name = new_name
    if 'description' in data:
        task.description = data['description']
    if 'due_date' in data:
        due_date = parse_date(data['due_date'])
        if data['due_date'] and not due_date:
            return jsonify({"error": "Fecha de vencimiento inválida (YYYY-MM-DD)."}), 400
        task.due_date = due_date
    if 'estado' in data:
        estado = EstadoTarea.query.filter_by(nombre=data['estado']).first()
        if not estado:
            return jsonify({'error': "Estado no existe"}), 400
        task.estado_id = estado.id

    db.session.commit()
    return jsonify({"message": "Tarea actualizada"}), 200

@task_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Tarea eliminada"}), 200
