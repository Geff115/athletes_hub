import os
from flask import Flask
from config import config
from extensions import db, migrate, login_manager


def create_app(config_name=None):
    if not config_name:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask(__name__)
    app.config_from_object(config[config_name])
    config[config_name].init_app(app)

    # Initializing extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    return app
