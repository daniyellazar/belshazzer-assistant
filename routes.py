from flask import Blueprint, request, jsonify
from config import gemini_model, switch_gemini_key, switch_openai_key
import openai
import logging

ai_route = Blueprint("ai_route", __name__)

@ai_route.route("/ai", methods=["POST"])
def ai():
    try:
        data = request.get_json()
        user_input = data.get("prompt", "").strip()

        if not user_input:
            return jsonify(error="⚠️ No prompt provided."), 400

        # --- Try Gemini first ---
        if gemini_model:
            try:
                response = gemini_model.generate_content(user_input)
                return jsonify(response=response.text)

            except Exception as e:
                logging.warning(f"Gemini failed: {e}, switching key...")
                if switch_gemini_key():
                    try:
                        response = gemini_model.generate_content(user_input)
                        return jsonify(response=response.text)
                    except Exception as e2:
                        logging.error(f"Gemini retry failed: {e2}")

        # --- Fallback to OpenAI ---
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_input}]
            )
            return jsonify(response=response.choices[0].message.content)

        except Exception as e:
            logging.warning(f"OpenAI failed: {e}, switching key...")
            if switch_openai_key():
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": user_input}]
                    )
                    return jsonify(response=response.choices[0].message.content)
                except Exception as e2:
                    logging.error(f"OpenAI retry failed: {e2}")

        return jsonify(error="❌ All API keys exhausted."), 500

    except Exception as e:
        return jsonify(error=f"❌ Internal server error: {str(e)}"), 500
