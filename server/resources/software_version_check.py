from flask import request, jsonify
from flask_restful import Resource
from models import db, SoftwareVersionCheck, VersionCheckResult

class SoftwareVersionCheckResource(Resource):
    def post(self):
        """Perform a new software version check."""
        data = request.get_json()
        new_check = SoftwareVersionCheck(
            user_id=data['user_id'],
            software_id=data['software_id'],
        )
        db.session.add(new_check)
        db.session.commit()
        return jsonify({"message": "Version check created successfully"}), 201

    def get(self, check_id):
        """Retrieve a specific software version check by its ID."""
        check = SoftwareVersionCheck.query.get(check_id)
        if check:
            return jsonify(check.to_dict())
        else:
            return jsonify({"message": "Version check not found"}), 404
