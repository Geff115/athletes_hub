import os
from flask import Flask
from flask import render_template
from config import config
from .extensions import db, login_manager
from flask_migrate import Migrate
from app.auth import auth as auth_blueprint
from app.main import main as main_blueprint
from app.admin import admin as admin_blueprint


def create_app(config_name=None):
    if not config_name:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initializing extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)

    # Registering the blueprints for the application routes
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    # Handling errors for the routes
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('500.html'), 500

    return app
