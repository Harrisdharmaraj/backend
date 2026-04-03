from flask_sqlalchemy import SQLAlchemy

# Initialize the database here instead of extensions.py
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), nullable=True) # NEW: Username
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    profile_photo = db.Column(db.String(255), nullable=True) # NEW: Path to image in uploads folder
    
    # New Location Columns
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    location_string = db.Column(db.String(255), nullable=True)
    preferred_language = db.Column(db.String(50), default='English') # NEW

class Crop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False)
    crop_name = db.Column(db.String(100), nullable=False)
    sowing_date = db.Column(db.Date, nullable=False)
    harvest_date = db.Column(db.Date, nullable=False)
    
    # Link to the tasks table (Cascade deletes tasks if crop is deleted)
    tasks = db.relationship('CropTask', backref='crop', lazy=True, cascade="all, delete-orphan")

class CropTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop_id = db.Column(db.Integer, db.ForeignKey('crop.id', ondelete='CASCADE'), nullable=False)
    task_day = db.Column(db.Integer, nullable=False)
    task_date = db.Column(db.Date, nullable=False)
    task_title = db.Column(db.String(255), nullable=False)
    task_description = db.Column(db.Text, nullable=False)
    is_completed = db.Column(db.Boolean, default=False)

# --- NEW LOCAL RESOURCE HUB TABLE ---


class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False)
    owner_name = db.Column(db.String(100), nullable=False)
    owner_phone = db.Column(db.String(15), nullable=False)
    item_name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), nullable=False) # e.g., 'Machinery', 'Fertilizer', 'Other'
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    is_available = db.Column(db.Boolean, default=True) # NEW: For the Out of Stock switch
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())