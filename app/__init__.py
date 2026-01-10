from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login"


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dash_bp
    from app.routes.api import api_bp
    from app.routes.api_commands import cmd_bp
    from app.routes.api_pubnub import pubnub_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dash_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(cmd_bp)
    app.register_blueprint(pubnub_bp)

    return app
