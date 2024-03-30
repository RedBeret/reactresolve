from flask import request, jsonify, session
from flask_restful import Resource
from models import db, UserAuth, bcrypt
from flask_bcrypt import generate_password_hash, check_password_hash

class UserAuthResource(Resource):
    def post(self):
        """Register a new user."""
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if UserAuth.query.filter_by(username=username).first() is not None:
            return jsonify({"message": "Username already exists"}), 400

        if UserAuth.query.filter_by(email=email).first() is not None:
            return jsonify({"message": "Email already exists"}), 400

        hashed_password = generate_password_hash(password).decode('utf-8')
        new_user = UserAuth(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201

class UserLoginResource(Resource):
    def post(self):
        """Authenticate and log in a user."""
        data = request.get_json()
        user = UserAuth.query.filter_by(username=data['username']).first()

        if user and check_password_hash(user.password_hash, data['password']):
            session['user_id'] = user.id
            return jsonify({"message": "Logged in successfully"}), 200
        else:
            return jsonify({"message": "Invalid username or password"}), 401

class UserLogoutResource(Resource):
    def post(self):
        """Log out the current user."""
        session.pop('user_id', None)
        return jsonify({"message": "Logged out successfully"}), 200

class SessionCheckResource(Resource):
    def get(self):
        """Check if the user is logged in."""
        user_id = session.get('user_id')
        if user_id:
            return jsonify({"logged_in": True}), 200
        else:
            return jsonify({"logged_in": False}), 200
