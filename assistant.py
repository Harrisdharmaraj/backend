from google import genai
from google.genai import types
from flask import Blueprint, request, jsonify
import base64
import json
from datetime import datetime, timedelta, date
from models import db, Crop, CropTask
import math
from models import db, Crop, CropTask, Resource
import urllib.request
import xml.etree.ElementTree as ET

assistant_bp = Blueprint('assistant_bp', __name__)

client = genai.Client(api_key="AIzaSyDJxnuifvOu3EfJTFazAea5e8ooMfCCM-o")

@assistant_bp.route("/ask", methods=["POST"])
def ask_assistant():
    data = request.get_json()
    user_message = data.get('message', '')
    language = data.get('language', 'English')
    location = data.get('location', '')
    image_base64 = data.get('imageBase64')

    if not user_message and not image_base64:
        return jsonify({"error": "Message or image is required"}), 400

    system_instruction = f"""
    You are AgroNova AI, a helpful agricultural expert.
    
    RULES:
    1. ALWAYS reply in {language}.
    2. Respond ONLY to agriculture, crops, farming, market prices, and weather.
    3. For anything else, politely say: "I am an agricultural assistant. Please ask me about farming." in {language}.
    4. LOCATION USAGE: The user's current location is "{location}". 
       - If {location} is empty, "Tap to set location", or "Not provided", and the user asks for local info (like weather or prices), ask them to set their location on the Home page first.
       - If a real location is provided, use it to give specific advice for that region.
    """

    try:
        contents = []
        if user_message:
            contents.append(user_message)
            
        if image_base64:
            image_bytes = base64.b64decode(image_base64)
            contents.append(types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg'))

        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=[{"google_search": {}}] 
            )
        )
        
        return jsonify({"reply": response.text}), 200
        
    except Exception as e:
        error_msg = str(e)
        print(f"Error calling Gemini: {error_msg}")
        
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            return jsonify({"reply": "I am receiving too many requests right now! Please wait about a minute and try asking me again."}), 200
            
        return jsonify({"error": "Failed to generate response. Please try again."}), 500

@assistant_bp.route("/scan-disease", methods=["POST"])
def scan_disease():
    data = request.get_json()
    language = data.get('language', 'English')
    image_base64 = data.get('imageBase64')

    if not image_base64:
        return jsonify({"error": "Image is required"}), 400

    system_instruction = f"""
    You are an expert plant pathologist and botanist.
    Analyze the uploaded image for crop or plant diseases.
    You MUST respond entirely in {language}.
    You MUST format your response STRICTLY as a valid JSON object. Do not include any markdown tags like ```json.
    Use this exact JSON structure:
    {{
        "diseaseName": "Name of the disease (or 'Healthy Plant')",
        "confidence": "A percentage like '98% Confidence'",
        "description": "A short 2-sentence description of the disease.",
        "treatmentSteps": ["Step 1", "Step 2", "Step 3"]
    }}
    """

    try:
        image_bytes = base64.b64decode(image_base64)
        contents = [types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg')]

        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2 
            )
        )
        
        raw_text = response.text.replace('```json', '').replace('```', '').strip()
        parsed_json = json.loads(raw_text)
        
        return jsonify(parsed_json), 200
        
    except Exception as e:
        print(f"Disease Scan Error: {e}")
        return jsonify({"error": "Failed to analyze image."}), 500

@assistant_bp.route("/translate-chemical", methods=["POST"])
def translate_chemical():
    data = request.get_json()
    language = data.get('language', 'English')
    image_base64 = data.get('imageBase64')

    if not image_base64:
        return jsonify({"error": "Image is required"}), 400

    system_instruction = f"""
    You are an expert agricultural chemist and safety advisor.
    Analyze the uploaded image of an agricultural chemical, pesticide, fertilizer, or herbicide label.
    You MUST respond entirely in {language}.
    You MUST format your response STRICTLY as a valid JSON object. Do not include any markdown tags like ```json.
    
    Determine the "toxicityLevel" and use ONLY one of these exact English words for that specific field (do not translate this field): "Organic", "Low", "Medium", "High".
    
    Use this exact JSON structure:
    {{
        "chemicalName": "Name of the product or active ingredient",
        "toxicityLevel": "High",
        "purpose": "A short 1-sentence description of what this kills or helps.",
        "dosage": "Clear instructions on how much to mix with water.",
        "timing": "When is the best time to apply it?",
        "safetyWarnings": ["Warning 1", "Warning 2", "Warning 3"]
    }}
    """

    try:
        image_bytes = base64.b64decode(image_base64)
        contents = [types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg')]

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.1 
            )
        )
        
        raw_text = response.text.replace('```json', '').replace('```', '').strip()
        parsed_json = json.loads(raw_text)
        
        return jsonify(parsed_json), 200
        
    except Exception as e:
        print(f"Chemical Translate Error: {e}")
        return jsonify({"error": "Failed to analyze chemical label."}), 500
    
@assistant_bp.route("/generate-calendar", methods=["POST"])
def generate_calendar():
    data = request.get_json()
    email = data.get('email')
    crop_name = data.get('cropName')
    sowing_date_str = data.get('sowingDate') 

    if not all([email, crop_name, sowing_date_str]):
        return jsonify({"error": "Missing data"}), 400

    system_instruction = f"""
    You are an expert agronomist. 
    Generate a concise, day-by-day cultivation schedule for planting {crop_name}.
    Return STRICTLY as a valid JSON object. No markdown tags.
    Format:
    {{
        "totalDaysToHarvest": 90,
        "tasks": [
            {{"day": 1, "title": "Initial Watering", "desc": "Lightly water the seeds."}},
            {{"day": 15, "title": "Apply Fertilizer", "desc": "Apply 50g Urea per 10L water."}}
        ]
    }}
    Make sure to include roughly 6 to 10 major milestone tasks spread across the growth cycle.
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[f"Generate a cultivation schedule for {crop_name}."],
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.1
            )
        )
        
        raw_text = response.text.replace('```json', '').replace('```', '').strip()
        calendar_data = json.loads(raw_text)
        
        sowing_date_obj = datetime.strptime(sowing_date_str, '%Y-%m-%d').date()
        harvest_date_obj = sowing_date_obj + timedelta(days=calendar_data['totalDaysToHarvest'])

        new_crop = Crop(user_email=email, crop_name=crop_name, sowing_date=sowing_date_obj, harvest_date=harvest_date_obj)
        db.session.add(new_crop)
        db.session.commit()
        
        tasks_to_return = []
        for task in calendar_data['tasks']:
            task_date_obj = sowing_date_obj + timedelta(days=task['day'])
            new_task = CropTask(
                crop_id=new_crop.id,
                task_day=task['day'],
                task_date=task_date_obj,
                task_title=task['title'],
                task_description=task['desc']
            )
            db.session.add(new_task)
            db.session.commit()
            
            tasks_to_return.append({
                "id": new_task.id,
                "cropId": new_crop.id,
                "day": new_task.task_day,
                "date": str(new_task.task_date),
                "title": new_task.task_title,
                "description": new_task.task_description,
                "isCompleted": new_task.is_completed
            })

        return jsonify({
            "cropId": new_crop.id, 
            "cropName": crop_name, 
            "sowingDate": str(sowing_date_obj),
            "harvestDate": str(harvest_date_obj), 
            "tasks": tasks_to_return
        }), 200

    except Exception as e:
        print(f"Calendar Gen Error: {e}")
        return jsonify({"error": "Failed to generate calendar."}), 500

@assistant_bp.route("/get-calendar", methods=["GET"])
def get_calendar():
    email = request.args.get('email')
    if not email:
        return jsonify({"error": "Email required"}), 400
        
    try:
        crops = Crop.query.filter_by(user_email=email).all()
        cutoff_date = date.today() - timedelta(days=3)
        
        response_data = []
        for crop in crops:
            CropTask.query.filter(
                CropTask.crop_id == crop.id,
                CropTask.is_completed == False,
                CropTask.task_date < cutoff_date
            ).delete()
            db.session.commit()

            tasks = CropTask.query.filter_by(crop_id=crop.id).order_by(CropTask.task_date.asc()).all()
            
            task_list = [{
                "id": t.id, 
                "cropId": t.crop_id, 
                "day": t.task_day,
                "date": str(t.task_date), 
                "title": t.task_title, 
                "description": t.task_description, 
                "isCompleted": t.is_completed
            } for t in tasks]
            
            response_data.append({
                "cropId": crop.id, 
                "cropName": crop.crop_name, 
                "sowingDate": str(crop.sowing_date), 
                "harvestDate": str(crop.harvest_date), 
                "tasks": task_list
            })
            
        return jsonify(response_data), 200
        
    except Exception as e:
        print(f"Get Calendar Error: {e}")
        return jsonify({"error": "Failed to fetch calendar."}), 500

@assistant_bp.route("/mark-task", methods=["POST"])
def mark_task():
    try:
        task_id = request.get_json().get('taskId')
        task = CropTask.query.get(task_id)
        if task:
            task.is_completed = True
            db.session.commit()
            return jsonify({"message": "Task marked complete."}), 200
        return jsonify({"error": "Task not found"}), 404
    except Exception as e:
        print(f"Mark Task Error: {e}")
        return jsonify({"error": "Failed to update task."}), 500
    
# --- LOCAL MARKET PREDICTION ROUTE ---

# --- LOCAL MARKET PREDICTION ROUTE ---

@assistant_bp.route("/market-prediction", methods=["GET"])
def market_prediction():
    location = request.args.get('location', 'Unknown')
    language = request.args.get('language', 'English')

    system_instruction = f"""
    You are an expert agricultural economist. 
    Analyze current market trends and weather data for {location}.
    You MUST respond entirely in {language}.
    You MUST format your response STRICTLY as a valid JSON object. Do not include markdown tags like ```json.
    Use this exact JSON structure:
    {{
        "summary": "A short 2-sentence summary of the overall market and weather situation.",
        "trends": [
            {{
                "cropName": "Name of crop (e.g. Tomato)",
                "emoji": "🍅", 
                "trend": "UP or DOWN",
                "percentage": "e.g. 15%",
                "reason": "1 short sentence explaining why."
            }}
        ]
    }}
    Provide exactly 3 to 4 crop trends.
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[f"Give me a crop market prediction and sowing advice for {location}."],
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=[{"google_search": {}}], 
                temperature=0.2
            )
        )
        
        raw_text = response.text.replace('```json', '').replace('```', '').strip()
        parsed_json = json.loads(raw_text)
        return jsonify({"data": parsed_json}), 200
        
    except Exception as e:
        error_msg = str(e)
        print(f"Market Prediction Error: {error_msg}")
        # Gracefully handle the 429 Quota Error so the Android app knows!
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            return jsonify({"error": "QUOTA_EXHAUSTED"}), 200
            
        return jsonify({"error": "Failed to generate market prediction."}), 500

# --- LOCAL RESOURCE HUB ROUTES ---

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0 
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@assistant_bp.route("/post-resource", methods=["POST"])
def post_resource():
    try:
        data = request.get_json()
        print("DATA RECEIVED:", data) 
        new_resource = Resource(
            user_email=data['email'],
            owner_name=data['ownerName'],
            owner_phone=data['ownerPhone'],
            item_name=data['itemName'],
            category=data['category'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            is_available=True
        )
        db.session.add(new_resource)
        db.session.commit()
        return jsonify({"message": "Resource posted successfully!"}), 200
    except Exception as e:
        print(f"Post Resource Error: {e}")
        return jsonify({"error": "Failed to post resource."}), 500

@assistant_bp.route("/get-resources", methods=["GET"])
def get_resources():
    try:
        user_lat = float(request.args.get('lat', 0.0))
        user_lon = float(request.args.get('lon', 0.0))
        
        resources = Resource.query.all()
        result_list = []
        
        for r in resources:
            dist = haversine_distance(user_lat, user_lon, r.latitude, r.longitude)
            if dist <= 50.0:
                result_list.append({
                    "id": r.id,
                    "userEmail": r.user_email,
                    "ownerName": r.owner_name,
                    "ownerPhone": r.owner_phone,
                    "itemName": r.item_name,
                    "category": r.category,
                    "isAvailable": r.is_available,
                    "distanceKm": round(dist, 1)
                })
        
        result_list.sort(key=lambda x: x['distanceKm'])
        return jsonify(result_list), 200
        
    except Exception as e:
        print(f"Get Resources Error: {e}")
        return jsonify({"error": "Failed to fetch resources."}), 500

@assistant_bp.route("/edit-resource", methods=["POST"])
def edit_resource():
    try:
        data = request.get_json()
        r = Resource.query.get(data['id'])
        if r:
            r.item_name = data['itemName']
            r.category = data['category']
            r.is_available = data['isAvailable']
            db.session.commit()
            return jsonify({"message": "Resource updated!"}), 200
        return jsonify({"error": "Not found"}), 404
    except Exception as e:
        return jsonify({"error": "Failed to update."}), 500

@assistant_bp.route("/delete-resource", methods=["POST"])
def delete_resource():
    try:
        data = request.get_json()
        r = Resource.query.get(data['id'])
        if r:
            db.session.delete(r)
            db.session.commit()
            return jsonify({"message": "Deleted successfully!"}), 200
        return jsonify({"error": "Not found"}), 404
    except Exception as e:
        return jsonify({"error": "Failed to delete."}), 500
    
# --- TOOLS & HUB ROUTES ---

@assistant_bp.route("/agri-news", methods=["GET"])
def agri_news():
    try:
        language = request.args.get('language', 'English')
        
        # Map Android languages to Google News Codes and Local Keywords
        lang_map = {
            "Tamil": ("ta", "IN:ta", "விவசாயம்"), 
            "Hindi": ("hi", "IN:hi", "कृषि"), 
            "Telugu": ("te", "IN:te", "వ్యవసాయం"),
            "Malayalam": ("ml", "IN:ml", "കൃഷി"),
            "Kannada": ("kn", "IN:kn", "ಕೃഷി"),
            "English": ("en-IN", "IN:en", "agriculture farming India")
        }
        
        hl, ceid, query = lang_map.get(language, ("en-IN", "IN:en", "agriculture farming India"))
        import urllib.parse
        q_encoded = urllib.parse.quote(query)
        
        # Dynamically fetch regional news!
        url = f"https://news.google.com/rss/search?q={q_encoded}&hl={hl}&gl=IN&ceid={ceid}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
        
        root = ET.fromstring(xml_data)
        news_items = []
        
        # Fetch top 15 news items
        for item in root.findall('./channel/item')[:15]:
            title = item.find('title').text if item.find('title') is not None else "Agri News"
            link = item.find('link').text if item.find('link') is not None else ""
            pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ""
            
            # Clean up the title format
            source = "Agri News"
            if " - " in title:
                parts = title.rsplit(" - ", 1)
                title = parts[0]
                source = parts[1]

            news_items.append({
                "title": title,
                "source": source,
                "link": link,
                "pubDate": pub_date
            })
        return jsonify(news_items), 200
    except Exception as e:
        print(f"News Fetch Error: {str(e)}")
        return jsonify([]), 200 # Return empty list gracefully if it fails

@assistant_bp.route("/calculate-farm-inputs", methods=["POST"])
def calculate_farm_inputs():
    data = request.get_json()
    crop_name = data.get('cropName')
    land_size = data.get('landSize')
    unit = data.get('unit')
    language = data.get('language', 'English')

    system_instruction = f"""
    You are an expert agronomist. 
    Calculate the exact seed rate and fertilizer (NPK/Urea/DAP) required for growing {crop_name} on {land_size} {unit}.
    Respond entirely in {language}.
    Format strictly as JSON. No markdown tags. Use this structure:
    {{
        "seedRequirement": "e.g., 2.5 kg of seeds or 18,500 seedlings",
        "fertilizerRequirement": "e.g., 100 kg Urea (2 Bags), 50 kg DAP (1 Bag)",
        "proTip": "1 short sentence of advice for this specific crop."
    }}
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[f"Calculate inputs for {crop_name} on {land_size} {unit}."],
            config=types.GenerateContentConfig(system_instruction=system_instruction, temperature=0.1)
        )
        raw_text = response.text.replace('```json', '').replace('```', '').strip()
        parsed_json = json.loads(raw_text)
        return jsonify({"data": parsed_json}), 200
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            return jsonify({"error": "QUOTA_EXHAUSTED"}), 200
        return jsonify({"error": "Failed to calculate inputs."}), 500