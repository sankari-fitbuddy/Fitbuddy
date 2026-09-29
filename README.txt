# FitBuddy Merged Project

This is the merged version of the separate FitBuddy modules.

Run from this folder:

    python -m pip install -r requirements.txt
    python -m uvicorn app.main:app --reload

Open:

    http://127.0.0.1:8000

Main flow:
Home -> Generate Workout -> Result -> Feedback -> Updated Plan
Progress -> Save/View progress and feedback
Admin -> View users/plans and delete users

Important:
1. Create a `.env` file in the project root.
2. Put your own Gemini API key in it:
   GEMINI_API_KEY=YOUR_KEY_HERE

Do not share your `.env` file publicly.
