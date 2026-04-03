import os
from flask import Flask, send_from_directory
from flask_cors import CORS  # ✅ NEW

from models import db
from models import User
from signup import signup_bp
from login import login_bp
from assistant import assistant_bp
from location_routes import location_bp
from profile_routes import profile_bp
from flask import render_template
from crop_routes import crop_bp

app = Flask(__name__)

# ✅ ENABLE CORS
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/agronova'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Upload folder
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Init DB
db.init_app(app)

# Blueprints
app.register_blueprint(signup_bp)
app.register_blueprint(login_bp)
app.register_blueprint(assistant_bp)
app.register_blueprint(location_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(crop_bp)

# Create tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)