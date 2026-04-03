import re
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from models import db, User

signup_bp = Blueprint('signup_bp', __name__)

@signup_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    
    name = data.get('name', '')
    email = data.get('email', '')
    phone = data.get('phone', '')
    password = data.get('password', '')

    # 1. Validation Rules
    if not re.match(r"^[A-Za-z]+$", name):
        return jsonify({"message": "Invalid name. Only letters allowed."}), 400
        
    if not re.match(r"^[A-Za-z0-9._%+-]+@(gmail\.com|mail\.com|saveetha\.com)$", email):
        return jsonify({"message": "Invalid email domain."}), 400
        
    if not re.match(r"^[0-9]{10}$", phone):
        return jsonify({"message": "Phone number must be exactly 10 digits."}), 400
        
    if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,8}$", password):
        return jsonify({"message": "Password does not meet complexity requirements."}), 400

    # 2. Check for existing user
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already registered."}), 409

    # 3. Hash the password
    # generate_password_hash converts "MyPass123!" into a secure string like "scrypt:32768:8:1$..."
    hashed_pw = generate_password_hash(password)
    
    # 4. Save to Database
    new_user = User(name=name, email=email, phone=phone, password_hash=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201