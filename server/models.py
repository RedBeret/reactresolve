import re
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class UserAuth(db.Model):
    __tablename__ = "user_auth"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    mfa_enabled = db.Column(db.Boolean, default=False)

    chat_messages = db.relationship("ChatMessage", back_populates="user")
    sessions = db.relationship("UserSession", back_populates="user")
    version_checks = db.relationship("SoftwareVersionCheck", back_populates="user")

    @validates('email', 'username')
    def validate_field(self, key, value):
        if key == "email":
            assert len(value) >= 3, "Email must be at least 3 characters long"
            assert re.match(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", value), "Invalid email format"
        elif key == "username":
            assert len(value) >= 3, "Username must be at least 3 characters long"
        return value

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class ChatMessage(db.Model):
    __tablename__ = "chat_messages"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_auth.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("UserAuth", back_populates="chat_messages")

class UserSession(db.Model):
    __tablename__ = "user_sessions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_auth.id'), nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ended_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship("UserAuth", back_populates="sessions")

class Software(db.Model):
    __tablename__ = "software"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    version_checks = db.relationship("SoftwareVersionCheck", back_populates="software")

class SoftwareVersionCheck(db.Model):
    __tablename__ = "software_version_checks"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_auth.id'), nullable=False)
    software_id = db.Column(db.Integer, db.ForeignKey('software.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("UserAuth", back_populates="version_checks")
    software = db.relationship("Software", back_populates="version_checks")
    result = db.relationship("VersionCheckResult", back_populates="version_check", uselist=False)

class VersionCheckResult(db.Model):
    __tablename__ = "version_check_results"

    id = db.Column(db.Integer, primary_key=True)
    expected_version = db.Column(db.String(50), nullable=False)
    found_version = db.Column(db.String(50), nullable=False)
    pass_fail = db.Column(db.Boolean, nullable=False)
    version_check_id = db.Column(db.Integer, db.ForeignKey('software_version_checks.id'), nullable=False)

    version_check = db.relationship("SoftwareVersionCheck", back_populates="result")
