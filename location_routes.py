from flask import Blueprint, request, jsonify
from models import db, User

location_bp = Blueprint('location_bp', __name__)

@location_bp.route("/update-location", methods=["POST"])
def update_location():
    data = request.get_json()
    
    email = data.get('email')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    location_string = data.get('location_string')

    if not email:
        return jsonify({"message": "Email is required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    try:
        user.latitude = latitude
        user.longitude = longitude
        user.location_string = location_string
        db.session.commit()
        return jsonify({"message": "Location updated successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Database error: {str(e)}"}), 500