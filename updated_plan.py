import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = None

if API_KEY:
    client = genai.Client(api_key=API_KEY)


def update_workout_plan(original_plan, feedback):

    if client is None:
        return original_plan + "\n\nGemini API key is not configured."

    prompt = f"""
Update this fitness workout plan based on the user's feedback.

Original workout plan:
{original_plan}

User feedback:
{feedback}

Return only the updated workout plan.
Keep it safe, simple and practical.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Gemini Error: {e}"