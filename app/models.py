from .database import db
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(64), unique=True, nullable=False)
    nombre_completo = db.Column(db.String(128), nullable=False)
    identificacion = db.Column(db.String(32), nullable=False)
    clave_hash = db.Column(db.String(128), nullable=False)  # SHA-256
    perfil = db.Column(db.String(32), nullable=False)
    tareas = db.relationship('Task', backref='usuario', lazy=True)

class EstadoTarea(db.Model):
    __tablename__ = "estado_tarea"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(32), unique=True, nullable=False)
    tareas = db.relationship('Task', backref='estado', lazy=True)

class Task(db.Model):
    __tablename__ = "tarea"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, default="")
    due_date = db.Column(db.Date, nullable=True)
    estado_id = db.Column(db.Integer, db.ForeignKey('estado_tarea.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
