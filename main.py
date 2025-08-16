from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import logging
import openai

# 🔐 Load environment variables
load_dotenv()

# Import models & key rotation from config.py
from config import gemini_model, switch_gemini_key, switch_openai_key

app = Flask(__name__)
CORS(app)

# 📝 Enable logging
logging.basicConfig(level=logging.INFO)

# 🎭 Personality styles
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

# 🤖 AI response endpoint
@app.route("/ai", methods=["POST"])
def ai():
    try:
        if not request.is_json:
            logging.warning("Request content-type is not JSON")
            return jsonify(error="⚠️ Request must be JSON"), 400

        data = request.get_json()
        user_input = data.get("prompt", "").strip()
        style_key = data.get("style", "")
        style = styles.get(style_key, "")

        if not user_input:
            return jsonify(error="⚠️ No prompt provided."), 400

        # 🧠 Construct prompt
        prompt = f"{style} Now respond to this: {user_input}" if style else user_input
        logging.info(f"Prompt: {prompt}")

        # 🌟 Try Gemini first
        try:
            response = gemini_model.generate_content(prompt)
            return jsonify(response=response.text)

        except Exception as gemini_error:
            logging.warning(f"Gemini failed: {gemini_error}")
            # 🔄 Switch Gemini key & retry once
            if switch_gemini_key():
                try:
                    response = gemini_model.generate_content(prompt)
                    return jsonify(response=response.text)
                except Exception as e2:
                    logging.error(f"Gemini retry failed: {e2}")

        # 🔄 Fallback to OpenAI
        try:
            openai_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            reply = openai_response.choices[0].message.content
            return jsonify(response=reply)

        except Exception as openai_error:
            logging.warning(f"OpenAI failed: {openai_error}")
            # 🔄 Switch OpenAI key & retry once
            if switch_openai_key():
                try:
                    openai_response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    reply = openai_response.choices[0].message.content
                    return jsonify(response=reply)
                except Exception as e2:
                    logging.error(f"OpenAI retry failed: {e2}")

        return jsonify(error="❌ All API keys exhausted."), 500

    except Exception as e:
        logging.error(f"Error in /ai endpoint: {str(e)}")
        return jsonify(error="❌ Internal server error"), 500

# 🧪 Health check
@app.route("/health")
def health():
    return jsonify(status="✅ OK", message="Assistant is running smoothly.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
