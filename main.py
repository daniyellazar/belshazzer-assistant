from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai
import os
import random
import logging

# 🔐 Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# 📝 Enable logging
logging.basicConfig(level=logging.INFO)

# 🔑 Load Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY not found in environment variables.")

# 🧠 Configure Gemini model
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# 🎭 Personality styles (optional fallback)
styles = {
    "bard": "Make it sound like a Shakespearean monologue.",
    "teen": "Respond with dry sarcasm and wit.",
    "coach": "Add a motivational twist like a life coach.",
    "joke": "Include a pun or joke before answering.",
    "oracle": "Speak like a futuristic oracle from the year 3025.",
    "poetic": "Be poetic and metaphorical in your reply.",
    "emoji": "Use emojis to express emotion and tone.",
    "question": "Ask the user a follow-up question at the end."
}

# 🏠 Serve frontend
@app.route("/")
def home():
    return render_template("index.html")

# 🤖 Gemini response endpoint
@app.route("/ai", methods=["POST"])
def ai():
    try:
        data = request.get_json()
        user_input = data.get("prompt", "").strip()
        style_key = data.get("style", "")
        style = styles.get(style_key, "")  # Use empty string if style not found

        if not user_input:
            return jsonify(error="⚠️ No prompt provided."), 400

        # 🧠 Construct prompt
        prompt = f"{style} Now respond to this: {user_input}" if style else user_input
        logging.info(f"Prompt sent to Gemini: {prompt}")

        response = model.generate_content(prompt)
        return jsonify(response=response.text)

    except Exception as e:
        logging.error(f"Error in /ai endpoint: {str(e)}")
        return jsonify(error=f"❌ Internal error: {str(e)}"), 500

# 🧪 Health check endpoint
@app.route("/health")
def health():
    return jsonify(status="✅ OK", message="Assistant is running smoothly.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)