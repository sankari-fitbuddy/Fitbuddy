import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_fitness_plan(goal, experience, days, feedback=""):

    prompt = f"""
    Create a safe, beginner-friendly fitness and healthy nutrition
    guidance plan for a teenager.

    Goal: {goal}
    Experience: {experience}
    Days per week: {days}
    Previous feedback: {feedback}
    Include:

    1. Weekly physical activity plan
       - Warm-up
       - Main activity
       - Rest/recovery days
       - Basic safety tips

    2. Healthy nutrition guidance
       - Balanced meals
       - Fruits and vegetables
       - Protein and whole grains
       - Water/hydration
       - Simple healthy snack ideas

    Important safety rules:
    - Do not give calorie targets.
    - Do not recommend restrictive diets.
    - Do not encourage skipping meals.
    - Do not promote rapid weight loss.
    - Keep the advice age-appropriate and general.
    - Encourage talking to a parent/guardian or qualified
      healthcare professional for personalized nutrition advice.

    Keep the plan simple and easy to follow.
    """

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            return (
                "Gemini quota temporarily exceeded. "
                "Please try again later."
            )

        return f"Gemini Error: {e}"