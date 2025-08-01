from app import create_app
from app.database import db
from app.models import Usuario
import hashlib

app = create_app()

with app.app_context():
    usuario_nuevo = Usuario(
        usuario='admin',
        nombre_completo='admin',
        identificacion='1234567',
        clave_hash=hashlib.sha256('adminpass'.encode()).hexdigest(),
        perfil='admin'
    )
    db.session.add(usuario_nuevo)
    db.session.commit()
    print("Usuario creado exitosamente")

