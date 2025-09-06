from flask import Flask, request, jsonify
import os
import google.generativeai as genai

app = Flask(__name__)

# Load API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    
    # Example Gemini response
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(user_message)
    
    return jsonify({"reply": response.text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
