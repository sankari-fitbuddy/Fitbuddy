import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_NAME = BASE_DIR / "fitbuddy.db"


def get_connection():
    return sqlite3.connect(str(DB_NAME))


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            age INTEGER,
            weight REAL,
            goal TEXT,
            intensity TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            workout_plan TEXT NOT NULL,
            updated_plan TEXT DEFAULT "",
            nutrition_tip TEXT DEFAULT ""
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            activity TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
            notes TEXT DEFAULT ""
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            feedback TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_user(user_id, username, age, weight, goal, intensity):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO users
        (user_id, username, age, weight, goal, intensity)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (str(user_id), username, age, weight, goal, intensity))
    conn.commit()
    conn.close()


def save_plan(user_id, workout_plan, nutrition_tip=""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO plans
        (user_id, workout_plan, updated_plan, nutrition_tip)
        VALUES (?, ?, ?, ?)
    """, (str(user_id), workout_plan, "", nutrition_tip))
    conn.commit()
    conn.close()


def update_plan(user_id, updated_plan):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM plans
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (str(user_id),))
    row = cursor.fetchone()

    if row:
        cursor.execute("""
            UPDATE plans
            SET updated_plan = ?
            WHERE id = ?
        """, (updated_plan, row[0]))

    conn.commit()
    conn.close()


def get_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_id, username, age, weight, goal, intensity
        FROM users WHERE user_id = ?
    """, (str(user_id),))
    user = cursor.fetchone()
    conn.close()
    return user


def get_original_plan(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT workout_plan
        FROM plans
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (str(user_id),))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None


def get_latest_plan(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, user_id, workout_plan, updated_plan, nutrition_tip
        FROM plans
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (str(user_id),))
    row = cursor.fetchone()
    conn.close()
    return row


def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_id, username, age, weight, goal, intensity
        FROM users
        ORDER BY rowid DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_all_plans():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, user_id, workout_plan, updated_plan, nutrition_tip
        FROM plans
        ORDER BY id ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def save_progress(name, activity, completed, notes=""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO progress (name, activity, completed, notes)
        VALUES (?, ?, ?, ?)
    """, (name, activity, completed, notes))
    conn.commit()
    conn.close()


def get_progress():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, activity, completed, notes
        FROM progress ORDER BY id DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def save_feedback(name, feedback):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO feedback (name, feedback)
        VALUES (?, ?)
    """, (name, feedback))
    conn.commit()
    conn.close()


def get_feedback():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, feedback
        FROM feedback ORDER BY id DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM plans WHERE user_id = ?", (str(user_id),))
    cursor.execute("DELETE FROM users WHERE user_id = ?", (str(user_id),))
    conn.commit()
    conn.close()


init_db()
