from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from gemini import generate_fitness_plan
import sqlite3

app = FastAPI()

templates = Jinja2Templates(directory="templates")


def init_db():
    conn = sqlite3.connect("fitbuddy.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            activity TEXT,
            completed INTEGER,
            notes TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            feedback TEXT
        )
    """)

    conn.commit()
    conn.close()


init_db()


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.post("/generate")
def generate(
    request: Request,
    name: str = Form(...),
    goal: str = Form(...),
    experience: str = Form(...),
    days: int = Form(...),
    feedback: str = Form("")
):
    try:
        plan = generate_fitness_plan(
            goal,
            experience,
            days,
            feedback
        )
    except Exception as e:
        print("ERROR:", repr(e))
        plan = f"Error: {e}"

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "plan": plan,
            "name": name
        }
    )


@app.get("/progress")
def progress_page(request: Request):
    conn = sqlite3.connect("fitbuddy.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, activity, completed, notes
        FROM progress
        ORDER BY id DESC
    """)

    progress_data = cursor.fetchall()

    cursor.execute("""
        SELECT name, feedback
        FROM feedback
        ORDER BY id DESC
    """)

    feedback_data = cursor.fetchall()

    conn.close()

    return templates.TemplateResponse(
        request=request,
        name="progress.html",
        context={
            "progress_data": progress_data,
            "feedback_data": feedback_data
        }
    )


@app.post("/progress")
def save_progress(
    name: str = Form(...),
    activity: str = Form(...),
    completed: int = Form(...),
    notes: str = Form("")
):
    conn = sqlite3.connect("fitbuddy.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO progress (name, activity, completed, notes)
        VALUES (?, ?, ?, ?)
        """,
        (name, activity, completed, notes)
    )

    conn.commit()
    conn.close()

    return RedirectResponse(
        url="/progress",
        status_code=303
    )


@app.post("/feedback")
def save_feedback(
    name: str = Form(...),
    feedback: str = Form(...)
):
    conn = sqlite3.connect("fitbuddy.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO feedback (name, feedback)
        VALUES (?, ?)
        """,
        (name, feedback)
    )

    conn.commit()
    conn.close()

    return RedirectResponse(
        url="/progress",
        status_code=303
    )