from flask import Blueprint, request, jsonify, current_app
from .models import Usuario
from .database import db
import jwt
import hashlib
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    usuario = data.get('usuario')
    clave = data.get('clave')
    if not usuario or not clave:
        return jsonify({'error': 'Usuario y clave requeridos'}), 400
    user = Usuario.query.filter_by(usuario=usuario).first()
    if not user or user.clave_hash != hash_password(clave):
        return jsonify({'error': 'Credenciales inválidas'}), 401
    payload = {
        'user_id': user.id,
        'usuario': user.usuario,
        'perfil': user.perfil,
        'exp': datetime.utcnow() + timedelta(hours=2)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({'token': token})

def token_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            parts = request.headers['Authorization'].split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                token = parts[1]
        if not token:
            return jsonify({'error': 'Token requerido'}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            request.user_id = data['user_id']
            request.usuario = data['usuario']
            request.perfil = data['perfil']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado'}), 401
        except Exception:
            return jsonify({'error': 'Token inválido'}), 401
        return f(*args, **kwargs)
    return decorated
