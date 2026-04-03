from flask import Blueprint, request, jsonify
from models import db, User
import base64
import os
import uuid
from werkzeug.security import check_password_hash, generate_password_hash

profile_bp = Blueprint('profile_bp', __name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

@profile_bp.route("/get-profile", methods=["GET"])
def get_profile():
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    image_base64 = None
    if user.profile_photo and os.path.exists(user.profile_photo):
        try:
            with open(user.profile_photo, "rb") as image_file:
                image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print("Error reading image:", e)

    return jsonify({
        "name": user.name,
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "profileImageBase64": image_base64
    }), 200

@profile_bp.route("/update-profile", methods=["POST"])
def update_profile():
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data.get('email')).first()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        user.name = data.get('name')
        user.username = data.get('username')
        user.phone = data.get('phone')
        
        # Handle Image Saving to 'uploads' folder
        image_base64 = data.get('profileImageBase64')
        if image_base64:
            # Create a unique filename
            filename = f"profile_{user.id}_{uuid.uuid4().hex[:8]}.jpg"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            
            # Decode and save physical file
            with open(filepath, "wb") as fh:
                fh.write(base64.b64decode(image_base64))
                
            # If user had an old photo, delete it to save space
            if user.profile_photo and os.path.exists(user.profile_photo):
                os.remove(user.profile_photo)
                
            user.profile_photo = filepath

        db.session.commit()
        return jsonify({"message": "Profile updated successfully!"}), 200
        
    except Exception as e:
        print("Update Profile Error:", e)
        return jsonify({"error": "Failed to update profile"}), 500

@profile_bp.route("/verify-password", methods=["POST"])
def verify_password():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    
    # Check if password matches (handling both raw and hashed passwords just in case)
    if user:
        try:
            is_match = check_password_hash(user.password_hash, data.get('currentPassword'))
        except:
            is_match = False
            
        if is_match or user.password_hash == data.get('currentPassword'):
            return jsonify({"message": "Verified"}), 200
            
    return jsonify({"error": "Incorrect current password"}), 401

@profile_bp.route("/change-password", methods=["POST"])
def change_password():
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data.get('email')).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        # Update with new hashed password
        user.password_hash = generate_password_hash(data.get('newPassword'))
        db.session.commit()
        return jsonify({"message": "Password changed successfully!"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to change password"}), 500

@profile_bp.route("/delete-account", methods=["POST"])
def delete_account():
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data.get('email')).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        # Delete profile photo from server if exists
        if user.profile_photo and os.path.exists(user.profile_photo):
            os.remove(user.profile_photo)
            
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Account deleted successfully"}), 200
    except Exception as e:
        print("Delete Account Error:", e)
        return jsonify({"error": "Failed to delete account"}), 500
    
@profile_bp.route("/update-language", methods=["POST"])
def update_language():
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data.get('email')).first()
        if user:
            user.preferred_language = data.get('language')
            db.session.commit()
            return jsonify({"message": "Language updated"}), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": "Failed to update language"}), 500