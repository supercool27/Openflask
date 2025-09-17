# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module


db = SQLAlchemy()
login_manager = LoginManager()


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('authentication', 'home', 'health','auth'): 
        module = import_module('apps.{}.routes'.format(module_name))
        if hasattr(module, 'blueprint'):
            app.register_blueprint(module.blueprint)
        elif hasattr(module, 'health_bp'):
            app.register_blueprint(module.health_bp)
        elif hasattr(module, 'auth_bp'):   
            app.register_blueprint(module.auth_bp)


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config["JWT_SECRET_KEY"] = "super-secret-key" 
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    return app
