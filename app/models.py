from flask_login import UserMixin
from datetime import datetime
import bcrypt
from app import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    pw_hash = db.Column(db.LargeBinary, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password: str):
        self.pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), self.pw_hash)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(64), unique=True, nullable=False, index=True)
    nickname = db.Column(db.String(64), default="My ClearDrop")
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    profile = db.Column(db.String(32), default="eczema")  
    temp_warn = db.Column(db.Float, default=38.0)
    temp_danger = db.Column(db.Float, default=40.0)
    tds_warn = db.Column(db.Integer, default=150)
    tds_danger = db.Column(db.Integer, default=250)


class Telemetry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(64), nullable=False, index=True)
    ts = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    temp_c = db.Column(db.Float, nullable=False)
    tds_ppm = db.Column(db.Integer, nullable=False)


class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(64), nullable=False, index=True)
    ts = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    level = db.Column(db.String(8), nullable=False)
    reason = db.Column(db.String(32), nullable=False)
    temp_c = db.Column(db.Float)
    tds_ppm = db.Column(db.Integer)
