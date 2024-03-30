from flask import request, jsonify
from flask_restful import Resource
from models import db, Software

class SoftwareResource(Resource):
    def get(self, software_id=None):
        """Retrieve all software or a specific one by its ID."""
        if software_id:
            software = Software.query.get(software_id)
            if software:
                return jsonify(software.to_dict())
            else:
                return jsonify({"message": "Software not found"}), 404
        else:
            all_software = Software.query.all()
            return jsonify([software.to_dict() for software in all_software]), 200

    def post(self):
        """Create a new software entry."""
        data = request.get_json()
        new_software = Software(name=data['name'])
        db.session.add(new_software)
        db.session.commit()
        return jsonify({"message": "Software created successfully", "software": new_software.to_dict()}), 201

    def delete(self, software_id):
        """Delete a software entry by its ID."""
        software = Software.query.get(software_id)
        if software:
            db.session.delete(software)
            db.session.commit()
            return jsonify({"message": "Software deleted successfully"}), 200
        else:
            return jsonify({"message": "Software not found"}), 404
