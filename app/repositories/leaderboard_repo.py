from fastapi import Query
from google.cloud import firestore  # Added import for firestore
from app.db.firebase import CONTEST_REF, QUESTION_REF, db, SUBMISSION_REF
from google.cloud.firestore import FieldFilter
from datetime import datetime, timedelta
import pytz

class LeaderboardRepository:
    @staticmethod
    def get_leaderboard(timeFrame: str = "week"):
        """Fetches the leaderboard data from Firestore based on the specified time frame."""
        now = datetime.utcnow()
        start_time = None

        if timeFrame == "today":
            start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif timeFrame == "week":
            start_time = now - timedelta(days=now.weekday())
            start_time = start_time.replace(hour=0, minute=0, second=0, microsecond=0)
        elif timeFrame == "month":
            start_time = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        query = SUBMISSION_REF.order_by("score", direction=firestore.Query.DESCENDING)
        
        if start_time:
            query = query.where("submission_time", ">=", start_time)

        submissions = []
        for doc in query.stream():
            sub = doc.to_dict()
            student = sub.get("student", {})
            
            # Convert time_spend to seconds if it's in hh:mm:ss format
            time_spend = sub.get("time_spend", 0)
            if isinstance(time_spend, str):
                try:
                    h, m, s = map(int, time_spend.split(':'))
                    time_spend = h * 3600 + m * 60 + s
                except:
                    time_spend = 0

            submissions.append({
                "user_id": student.get("telegram_id", "unknown"),
                "user_name": student.get("name", "Unknown"),
                "score": sub.get("score", 0),
                "correct_answers": sub.get("correct_answers", 0),
                "total_questions": sub.get("total_questions", 0),
                "time_taken": time_spend
            })

        # Add ranks
        for rank, entry in enumerate(submissions, 1):
            entry["rank"] = rank

        return submissions[:100]  # Limit to top 100