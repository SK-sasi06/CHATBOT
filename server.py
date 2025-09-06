# server.py
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# Load API key from environment
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY is not set. Please set it before running.")

# Configure Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Flask app
app = Flask(__name__)
CORS(app)

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        messages = data.get("messages", [])

        # Convert messages into Gemini format
        history = []
        for m in messages:
            if m["role"] == "user":
                history.append({"role": "user", "parts": [m["text"]]})
            else:
                history.append({"role": "model", "parts": [m["text"]]})

        # Get model response
        response = model.generate_content(history)
        reply = response.text if response else "No reply from model."

        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
