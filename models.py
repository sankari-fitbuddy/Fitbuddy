from .database import (
    save_user,
    get_user,
    get_all_users,
    save_plan,
    update_plan,
    get_original_plan,
    get_latest_plan,
    get_all_plans,
    save_progress,
    get_progress,
    save_feedback,
    get_feedback,
    delete_user
)


# ==========================================
# USER MODEL
# ==========================================

class User:

    @staticmethod
    def create(user_id, username, age, weight, goal, intensity):
        save_user(
            user_id,
            username,
            age,
            weight,
            goal,
            intensity
        )

    @staticmethod
    def get(user_id):
        return get_user(user_id)

    @staticmethod
    def get_all():
        return get_all_users()

    @staticmethod
    def delete(user_id):
        delete_user(user_id)


# ==========================================
# WORKOUT PLAN MODEL
# ==========================================

class Plan:

    @staticmethod
    def create(user_id, workout_plan, nutrition_tip=""):
        save_plan(
            user_id,
            workout_plan,
            nutrition_tip
        )

    @staticmethod
    def update(user_id, updated_plan):
        update_plan(
            user_id,
            updated_plan
        )

    @staticmethod
    def get_original(user_id):
        return get_original_plan(user_id)

    @staticmethod
    def get_latest(user_id):
        return get_latest_plan(user_id)

    @staticmethod
    def get_all():
        return get_all_plans()


# ==========================================
# PROGRESS MODEL
# ==========================================

class Progress:

    @staticmethod
    def create(name, activity, completed, notes=""):
        save_progress(
            name,
            activity,
            completed,
            notes
        )

    @staticmethod
    def get_all():
        return get_progress()


# ==========================================
# FEEDBACK MODEL
# ==========================================

class Feedback:

    @staticmethod
    def create(name, feedback):
        save_feedback(
            name,
            feedback
        )

    @staticmethod
    def get_all():
        return get_feedback()