from flask import Blueprint, request, jsonify
from google import genai

crop_bp = Blueprint("crop", __name__)

client = genai.Client(api_key="AIzaSyDJxnuifvOu3EfJTFazAea5e8ooMfCCM-o")

@crop_bp.route("/recommend-crop", methods=["POST"])
def recommend():

    data = request.get_json()

    soil = data.get("soil", "")
    season = data.get("season", "")
    water = data.get("water", "")

    prompt = f"""
    You are an agricultural expert.

    Soil type: {soil}
    Season: {season}
    Water availability: {water}

    Suggest best crops for this condition in India.
    Give:
    - Crop names
    - Short reason
    - Basic tips
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return jsonify({
        "result": response.text
    })