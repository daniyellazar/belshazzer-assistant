from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai
import os
import random

# 🔐 Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# 🔑 Load Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY not found in environment variables.")

# 🧠 Configure Gemini model
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# 🎭 Personality styles
styles = [
    "Respond with dry sarcasm and wit.",
    "Make it sound like a Shakespearean monologue.",
    "Add a motivational twist like a life coach.",
    "Include a pun or joke before answering.",
    "Speak like a futuristic oracle from the year 3025.",
    "Be poetic and metaphorical in your reply.",
    "Use emojis to express emotion and tone.",
    "Ask the user a follow-up question at the end."
]

@app.route("/")
def home():
    return "🧠 Belshazzar is online and evolving."

@app.route("/chat")
def chat():
    return render_template("index.html")

@app.route("/ai", methods=["POST"])
def ai():
    try:
        data = request.get_json()
        user_input = data.get("prompt", "").strip()

        if not user_input:
            return jsonify(error="⚠️ No prompt provided."), 400

        # 🎲 Inject a random style
        style = random.choice(styles)
        prompt = f"{style} Now respond to this: {user_input}"

        response = model.generate_content(prompt)
        return jsonify(response=response.text)

    except Exception as e:
        return jsonify(error=f"❌ Internal error: {str(e)}"), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)