from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from models import User

login_bp = Blueprint('login_bp', __name__)

@login_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    
    email = data.get('email', '')
    password = data.get('password', '')

    # Find the user by email
    user = User.query.filter_by(email=email).first()

    # check_password_hash safely compares the plain text password to the database hash
    if user and check_password_hash(user.password_hash, password):
        dummy_token = f"fake-jwt-token-for-{user.id}"
        
        # Safely get location data (returns None if not set yet)
        user_name = user.name
        loc_string = getattr(user, 'location_string', None)
        lat = getattr(user, 'latitude', None)
        lon = getattr(user, 'longitude', None)
        pref_lang = getattr(user, 'preferred_language', 'English') # NEW

        return jsonify({
            "message": "Login successful",
            "token": dummy_token,
            "name": user_name,
            "location_string": loc_string,
            "latitude": lat,
            "longitude": lon,
            "preferred_language": pref_lang # NEW
        }), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401