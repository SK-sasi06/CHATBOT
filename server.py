import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env (for local dev)
load_dotenv()

# Get Gemini API key
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY is not set. Please check your .env or Render environment variables.")

# Configure Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Flask app — tell Flask where to find templates and static files
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app, resources={r"/*": {"origins": "*"}})

# Serve the chatbot UI
@app.route("/")
def home():
    return render_template("index.html")

# Chat API endpoint
@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        messages = data.get("messages", [])

        # Convert messages to Gemini format
        history = [
            {"role": m["role"], "parts": [m["text"]]}
            for m in messages if m["role"] in ["user", "model"]
        ]

        # Get model response
        response = model.generate_content(history)
        reply = response.text if response else "No reply from model."

        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Health check route (optional)
@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
