import os
import itertools
import google.generativeai as genai
import openai

# --- Load Gemini keys ---
GEMINI_KEYS = [os.getenv(f"GEMINI_API_KEY_{i}") for i in range(1, 6)]
GEMINI_KEYS = [k for k in GEMINI_KEYS if k]

# --- Load OpenAI keys ---
OPENAI_KEYS = [os.getenv(f"OPENAI_API_KEY_{i}") for i in range(1, 6)]
OPENAI_KEYS = [k for k in OPENAI_KEYS if k]

if not GEMINI_KEYS and not OPENAI_KEYS:
    raise RuntimeError("❌ No API keys found in environment variables.")

# --- Setup cycles for rotation ---
gemini_cycle = itertools.cycle(GEMINI_KEYS) if GEMINI_KEYS else None
openai_cycle = itertools.cycle(OPENAI_KEYS) if OPENAI_KEYS else None

# --- Current keys ---
current_gemini_key = next(gemini_cycle) if gemini_cycle else None
current_openai_key = next(openai_cycle) if openai_cycle else None

# --- Configure Gemini ---
if current_gemini_key:
    genai.configure(api_key=current_gemini_key)
    gemini_model = genai.GenerativeModel("gemini-pro")
else:
    gemini_model = None

# --- Configure OpenAI ---
if current_openai_key:
    openai.api_key = current_openai_key


def switch_gemini_key():
    """Rotate to next Gemini key."""
    global current_gemini_key, gemini_model
    if gemini_cycle:
        current_gemini_key = next(gemini_cycle)
        genai.configure(api_key=current_gemini_key)
        gemini_model = genai.GenerativeModel("gemini-pro")
        return current_gemini_key
    return None


def switch_openai_key():
    """Rotate to next OpenAI key."""
    global current_openai_key
    if openai_cycle:
        current_openai_key = next(openai_cycle)
        openai.api_key = current_openai_key
        return current_openai_key
    return None
