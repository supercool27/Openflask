# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from importlib import import_module

db = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager()
migrate = Migrate()


def register_extensions(app):
    """Initialize Flask extensions"""
    db.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app)


def register_blueprints(app):
    """Register all blueprints dynamically"""
    for module_name in ('authentication', 'home', 'health', 'auth', 'quiz'):  
        module = import_module(f'apps.{module_name}.routes')
        
        if hasattr(module, 'blueprint'):
            app.register_blueprint(module.blueprint)
        elif hasattr(module, 'health_bp'):
            app.register_blueprint(module.health_bp)
        elif hasattr(module, 'auth_bp'):
            app.register_blueprint(module.auth_bp)
        elif hasattr(module, 'quiz_bp'):   # 👈 yahan se aapke quiz_bp ko register karega
            app.register_blueprint(module.quiz_bp)


def configure_database(app):
    """Database setup hooks"""

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def create_app(config):
    """Flask application factory"""
    app = Flask(__name__)
    app.config.from_object(config)

    # 👇 JWT secret key (move to env variable in production)
    app.config["JWT_SECRET_KEY"] = "super-secret-key"

    register_extensions(app)
    register_blueprints(app)
    configure_database(app)

    return app
