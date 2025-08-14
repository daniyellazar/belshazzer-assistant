from flask import Blueprint, request, jsonify
import random
from config import model

ai_route = Blueprint("ai_route", __name__)

styles = [
    "Respond like a Shakespearean bard:",
    "Answer as a sarcastic teenager:",
    "Speak like a wise monk:",
    "Reply with pirate slang:"
]

@ai_route.route("/ai", methods=["POST"])
def ai():
    try:
        data = request.get_json()
        user_input = data.get("prompt", "").strip()

        if not user_input:
            return jsonify(error="⚠️ No prompt provided."), 400

        style = random.choice(styles)
        prompt = f"{style} Now respond to this: {user_input}"

        response = model.generate_content(prompt)
        return jsonify(response=response.text)

    except Exception as e:
        return jsonify(error="❌ Internal server error."), 500