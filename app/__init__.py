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

    # Start PubNub subscriber AFTER app/db are initialized
    from app.iot_worker import start_iot_worker
    start_iot_worker(app)

    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.dashboard import dash_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(dash_bp)

    return app
