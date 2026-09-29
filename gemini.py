import os
import time
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
# BACKUP WORKOUT PLAN
# =========================================================

def backup_workout_plan(goal, intensity):

    return f"""
FITBUDDY WORKOUT PLAN

Goal: {goal}
Intensity: {intensity}


1. WARM-UP
--------------------
• Light walking - 5 minutes
• Arm circles - 10 repetitions
• Leg swings - 10 repetitions
• Shoulder rotations - 10 repetitions


2. MAIN WORKOUT
--------------------
• Bodyweight Squats
  3 sets × 10 repetitions

• Wall Push-ups
  3 sets × 10 repetitions

• Glute Bridges
  3 sets × 12 repetitions

• Marching in Place
  3 sets × 30 seconds

• Standing Knee Raises
  2 sets × 10 repetitions


3. COOL-DOWN
--------------------
• Gentle leg stretching - 30 seconds
• Shoulder stretching - 30 seconds
• Slow walking - 2 to 3 minutes


4. REST AND RECOVERY
--------------------
• Take adequate rest between workout days.
• Drink enough water.
• Get sufficient sleep.
• Increase workout intensity gradually.


5. SAFETY TIPS
--------------------
• Start slowly.
• Maintain proper exercise form.
• Do not exercise through pain.
• Stop if you feel dizzy or unusually uncomfortable.
• Beginners should increase intensity gradually.
"""


# =========================================================
# AI FITNESS PLAN
# =========================================================

def generate_fitness_plan(goal, intensity):

    # API key not configured
    if client is None:
        print("Gemini API key not configured. Using backup plan.")
        return backup_workout_plan(goal, intensity)

    prompt = f"""
You are FitBuddy, an AI fitness planner.

Create a safe, simple and practical workout plan.

User fitness goal:
{goal}

Workout intensity:
{intensity}

Create the workout plan with these sections:

1. Warm-up
2. Main Workout
3. Cool-down
4. Rest and Recovery
5. Safety Tips

Requirements:
- Keep it beginner-friendly.
- Keep exercises simple.
- Mention sets and repetitions where appropriate.
- Do not recommend dangerous exercises.
- Do not give medical advice.
- Keep the language easy to understand.
- Make the plan practical for home or basic gym use.
- Return ONLY the workout plan.
"""

    # Try Gemini up to 3 times
    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

            if response and response.text:
                return response.text

            print("Gemini returned empty response.")

        except Exception as e:

            error_text = str(e)

            print(f"Gemini attempt {attempt + 1} failed:")
            print(error_text)

            # Retry temporary errors
            if (
                "503" in error_text
                or "UNAVAILABLE" in error_text
                or "timeout" in error_text.lower()
                or "timed out" in error_text.lower()
            ):

                if attempt < 2:
                    time.sleep(3)
                    continue

    # Gemini failed -> backup plan
    print("Gemini unavailable. Using backup workout plan.")

    return backup_workout_plan(goal, intensity)


# =========================================================
# GEMINI STATUS
# =========================================================

def gemini_status():

    if client is None:
        return "Gemini API key is not configured."

    return "Gemini API is configured successfully."