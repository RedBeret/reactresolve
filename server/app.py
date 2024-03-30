from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_restful import Api
from config import Config
from flask_session import Session 

# Initialization
app = Flask(__name__)
app.config.from_object(Config)

# Extensions
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
api = Api(app)
migrate = Migrate(app, db)
Session(app)  

from models import UserAuth, Software, SoftwareVersionCheck, ChatMessage, UserSession, VersionCheckResult
from resources import (UserAuthResource, UserLoginResource, UserLogoutResource, SessionCheckResource,
                       SoftwareResource, SoftwareVersionCheckResource)

api.add_resource(UserAuthResource, '/api/users', '/api/users/<int:user_id>')
api.add_resource(UserLoginResource, '/api/login')
api.add_resource(UserLogoutResource, '/api/logout')
api.add_resource(SessionCheckResource, '/api/session')
api.add_resource(SoftwareResource, '/api/software', '/api/software/<int:software_id>')
api.add_resource(SoftwareVersionCheckResource, '/api/version_checks', '/api/version_checks/<int:check_id>')

@app.route('/')
def index():
    """Endpoint for testing the API's availability."""
    return jsonify({'message': 'Welcome to the Version Checker API'})

if __name__ == '__main__':
    app.run(debug=True)
