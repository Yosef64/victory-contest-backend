from fastapi import Query
from starlette.background import P
from app.db.firebase import CONTEST_REF, QUESTION_REF, db, SUBMISSION_REF
from google.cloud.firestore import FieldFilter
from datetime import datetime, timedelta
import pytz

class LeaderboardRepository:
    @staticmethod
    def get_leaderboard(timeFrame: str = "week"):
        """
        Fetches the leaderboard data from Firestore based on the specified time frame.
        """
        now = datetime.utcnow()
        start_time = None

        if timeFrame == "today":
            start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif timeFrame == "week":
            days_since_monday = now.weekday()
            start_time = now - timedelta(days=days_since_monday)
            start_time = start_time.replace(hour=0, minute=0, second=0, microsecond=0)
        elif timeFrame == "month":
            start_time = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Convert to Firestore timestamp format
        firestore_start_time = start_time.astimezone(pytz.utc) if start_time else None

        submissions_query = SUBMISSION_REF.order_by("score", direction="DESCENDING")

        if firestore_start_time:
            submissions_query = submissions_query.where(filter=FieldFilter("submission_time", ">=", firestore_start_time))

        submissions = [doc.to_dict() for doc in submissions_query.stream()]

        leaderboard_data = []
        rank = 1
        for submission in submissions:
            student = submission.get("student", {})
            user_id = student.get("Student_id") or student.get("student_id") or student.get("telegram_id") or "unknown"
            user_name = student.get("name", "Unknown")
            leaderboard_data.append({
                "user_id": user_id,
                "user_name": user_name,
                "rank": rank,
                "score": submission.get("score", 0),
                "correct_answers": submission.get("correct_answers", 0),
                "total_questions": submission.get("total_questions", 0),
                "time_taken": submission.get("time_spend", 0)
            })
            rank += 1

        return leaderboard_data