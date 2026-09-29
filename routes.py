from fastapi import APIRouter, Form, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from .database import (
    save_user,
    save_plan,
    update_plan,
    get_original_plan,
    get_user,
    get_latest_plan,
    get_all_users,
    get_all_plans,
    delete_user,
    save_progress,
    get_progress,
    save_feedback,
    get_feedback,
)
from .gemini import generate_fitness_plan
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .updated_plan import update_workout_plan

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/health")
def health_check():
    return {"status": "OK", "message": "FitBuddy API is working"}


@router.post("/generate-workout")
@router.post("/workout")
def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
):
    workout_plan = generate_fitness_plan(goal, intensity)
    nutrition_tip = generate_nutrition_tip_with_flash(goal)

    save_user(user_id, username, age, weight, goal, intensity)
    save_plan(user_id, workout_plan, nutrition_tip)

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "user_id": user_id,
            "username": username,
            "name": username,
            "age": age,
            "weight": weight,
            "goal": goal,
            "intensity": intensity,
            "workout": workout_plan,
            "workout_plan": workout_plan,
            "nutrition_tip": nutrition_tip,
        },
    )


@router.post("/nutrition-tip")
def nutrition_tip(
    username: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
):
    tip = generate_nutrition_tip_with_flash(goal)
    return {"username": username, "nutrition_tip": tip}


@router.post("/submit-feedback")
def submit_feedback(
    username: str = Form(...),
    user_id: str = Form(...),
    feedback: str = Form(...),
    original_plan: str = Form(...),
):
    try:
        updated = update_workout_plan(original_plan, feedback)
        update_plan(user_id, updated)

        return {
            "success": True,
            "username": username,
            "user_id": user_id,
            "feedback": feedback,
            "updated_plan": updated,
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)},
        )


@router.get("/result")
def result(
    request: Request,
    user_id: str = "",
    username: str = "",
):
    plan = get_latest_plan(user_id)

    workout = plan[3] if plan and plan[3] else (plan[2] if plan else "")
    nutrition_tip = plan[4] if plan and len(plan) > 4 else ""

    user = get_user(user_id)

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "user_id": user_id,
            "username": username or (user[1] if user else ""),
            "name": username or (user[1] if user else ""),
            "goal": user[4] if user else "",
            "intensity": user[5] if user else "",
            "workout": workout,
            "workout_plan": workout,
            "nutrition_tip": nutrition_tip,
        },
    )


@router.get("/progress")
def progress_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="progress.html",
        context={
            "progress_data": get_progress(),
            "feedback_data": get_feedback(),
        },
    )


@router.post("/progress")
def progress_post(
    name: str = Form(...),
    activity: str = Form(...),
    completed: int = Form(...),
    notes: str = Form(""),
):
    save_progress(name, activity, completed, notes)
    return RedirectResponse("/progress", status_code=303)


@router.post("/feedback")
def feedback_post(
    name: str = Form(...),
    feedback: str = Form(...),
):
    save_feedback(name, feedback)
    return RedirectResponse("/progress", status_code=303)


@router.get("/admin")
@router.get("/view-all-users")
def admin(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "users": get_all_users(),
            "plans": get_all_plans(),
        },
    )


@router.get("/all-workouts")
def all_workouts():
    return {"plans": get_all_plans()}


@router.delete("/delete-user/{user_id}")
def delete_user_route(user_id: str):
    delete_user(user_id)
    return {"message": "User deleted successfully", "user_id": user_id}
