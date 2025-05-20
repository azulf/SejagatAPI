from flask import Flask, request, jsonify
from utils import fetch_weather
from flask_cors import CORS
import redis
import json
import requests



app = Flask(__name__)

CORS(app)  # Enable CORS for all routes

r = redis.Redis(host='localhost', port=6379, db=0)

CACHE_EXPIRE = 600  # Cache expiration time in seconds

@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city") 
    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    # Check if the weather data is cached
    cached_data = r.get(city)
    if cached_data:
        return jsonify(cached_data), 200
    else :
        weather_data = fetch_weather(city)
        status_code = 200 if "error" not in weather_data else 400
        data_weather = {
            "city": weather_data.get("location", {}).get("name"),
            "temperature": weather_data.get("current", {}).get("temp_c"),
            "condition": weather_data.get("current", {}).get("condition", {}).get("text"),
            "icon": weather_data.get("current", {}).get("condition", {}).get("icon"),
        }

        # Cache the weather data
        r.setex(city, CACHE_EXPIRE, json.dumps(data_weather))

        return jsonify(data_weather), status_code



if __name__ == "__main__":
    app.run(port=5002,debug=True)