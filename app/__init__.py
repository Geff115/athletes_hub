import os
from flask import Flask
from flask import render_template
from config import config
from .extensions import db, login_manager
from flask_migrate import Migrate
from app.auth import auth as auth_blueprint
from app.main import main as main_blueprint
from app.admin import admin as admin_blueprint
from app.messaging.socket_handlers import socketio,  MessageNamespace
from app.messaging.socket_handlers import NotificationNamespace
from flask_uploads import UploadSet, configure_uploads, IMAGES, ALL



media = UploadSet('media', ALL)

def create_app(config_name=None):
    if not config_name:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Configuring file uploads
    if not os.path.exists(app.config['UPLOADED_MEDIA_DEST']): 
        os.makedirs(app.config['UPLOADED_MEDIA_DEST'])

    app.config['UPLOADED_MEDIA_DEST'] = 'uploads/media'
    configure_uploads(app, media)

    # Initializing extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    socketio.init_app(app)

    # Registering the blueprints for the application routes
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    
    # Registering the WebSocket namespace
    socketio.on_namespace(MessageNamespace('/messages'))
    socketio.on_namespace(NotificationNamespace('/notifications'))

    # Handling errors for the routes
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('500.html'), 500

    return app
