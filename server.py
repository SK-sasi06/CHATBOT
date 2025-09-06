# server.py — Clean version for Render deployment

from flask import Flask, request, jsonify
import os
import google.generativeai as genai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend (Netlify) to connect

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("⚠️ GEMINI_API_KEY is not set!")
genai.configure(api_key=api_key)

@app.route("/", methods=["GET"])
def home():
    return "✅ Gemini Chatbot Backend is running!"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"reply": "⚠️ Please send a message."})

        # Generate response using Gemini
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(user_message)

        return jsonify({"reply": response.text})

    except Exception as e:
        print("Error in /chat:", e)
        return jsonify({"reply": "⚠️ Server error. Please try again later."})

if __name__ == "__main__":
    # Use host=0.0.0.0 for Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
