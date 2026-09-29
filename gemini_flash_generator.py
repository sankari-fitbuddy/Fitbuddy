import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


# =========================================================
# LOAD .ENV
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)

API_KEY = os.getenv("GEMINI_API_KEY")


# =========================================================
# GEMINI CLIENT
# =========================================================

if API_KEY:
    client = genai.Client(
        api_key=API_KEY,
        http_options=types.HttpOptions(
            timeout=120000
        )
    )
else:
    client = None


# =========================================================
# BACKUP NUTRITION TIP
# =========================================================

def backup_nutrition_tip(goal):

    goal_text = str(goal).lower()

    if "weight" in goal_text and "loss" in goal_text:

        return """
Nutrition Tip:

Choose balanced meals with vegetables, protein,
whole grains, and enough water. Focus on regular
meals and reasonable portions instead of extreme
dieting.
"""

    if "muscle" in goal_text or "gain" in goal_text:

        return """
Nutrition Tip:

Include a good source of protein in your meals,
along with whole grains, vegetables, fruits, and
enough water. Consistent nutrition and adequate
rest support muscle-building goals.
"""

    if "fitness" in goal_text or "general" in goal_text:

        return """
Nutrition Tip:

Build balanced meals using protein, vegetables,
fruits, whole grains, and healthy fats. Stay
hydrated throughout the day and maintain regular
eating habits.
"""

    return """
Nutrition Tip:

Choose balanced meals with protein, vegetables,
fruits, whole grains, and enough water. Focus on
consistent healthy food choices and avoid extreme
diets.
"""


# =========================================================
# AI NUTRITION TIP
# =========================================================

def generate_nutrition_tip_with_flash(goal):

    # API key unavailable
    if client is None:
        print("Gemini API key not configured. Using backup nutrition tip.")
        return backup_nutrition_tip(goal)

    prompt = f"""
You are FitBuddy, an AI fitness and nutrition assistant.

User fitness goal:
{goal}

Give ONE simple and practical nutrition tip that supports
this fitness goal.

Requirements:
- Keep it short.
- Use simple English.
- Make it safe and practical.
- Do not give medical advice.
- Do not recommend extreme diets.
- Return ONLY the nutrition tip.
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        if response and response.text:
            return response.text

        return backup_nutrition_tip(goal)

    except Exception as e:

        print("Nutrition Gemini error:")
        print(str(e))

        # Gemini busy / unavailable
        return backup_nutrition_tip(goal)