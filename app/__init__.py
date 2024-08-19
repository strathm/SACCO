from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
socketio = SocketIO()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    socketio.init_app(app)

    from app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.routes.loans import bp as loans_bp
    app.register_blueprint(loans_bp, url_prefix='/loans')

    from app.routes.savings import bp as savings_bp
    app.register_blueprint(savings_bp, url_prefix='/savings')

    from app.routes.meetings import bp as meetings_bp
    app.register_blueprint(meetings_bp, url_prefix='/meetings')

    from app.routes.notifications import bp as notifications_bp
    app.register_blueprint(notifications_bp, url_prefix='/notifications')

    from app.routes.projects import bp as projects_bp
    app.register_blueprint(projects_bp, url_prefix='/projects')

    from app.routes.investments import bp as investments_bp
    app.register_blueprint(investments_bp, url_prefix='/investments')

    return app
