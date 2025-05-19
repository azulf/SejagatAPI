from flask import Flask, request, jsonify
from utils import fetch_weather

app = Flask(__name__)

@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City parameter is required"}), 400
    weather_data = fetch_weather(city)
    status_code = 200 if "error" not in weather_data else 400
    return jsonify(weather_data), status_code

if __name__ == "__main__":
    app.run(port=8080,debug=True)