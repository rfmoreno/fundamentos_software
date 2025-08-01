from flask import Flask
from .database import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/taskdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'cambia-esto-por-una-clave-secreta-larga'

    db.init_app(app)

    from .routes import task_bp
    from .auth import auth_bp

    app.register_blueprint(task_bp, url_prefix='/api/tasks')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    with app.app_context():
        db.create_all()
    return app
