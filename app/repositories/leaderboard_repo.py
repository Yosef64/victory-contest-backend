from zoneinfo import ZoneInfo
from app.db.firebase import SUBMISSION_REF
from datetime import datetime, timedelta

class LeaderboardRepository:
    def format_seconds_to_hms(seconds: int) -> str:
        """Converts a total number of seconds into an HH:MM:SS string."""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        if hours > 0:
            return f"{int(hours)}:{int(minutes):02}:{int(secs):02}"
        else:
            return f"{int(minutes):02}:{int(secs):02}"
    @staticmethod
    def get_leaderboard(timeFrame: str = "week"):
        """
        Fetches the top 100 leaderboard entries by aggregating all submissions
        from each user within the specified time frame.
        """
        TARGET_TZ = ZoneInfo("Africa/Addis_Ababa")
        now_local = datetime.now(TARGET_TZ)
        
        start_time = None

        if timeFrame == "today":
            start_time = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
        elif timeFrame == "week":
            start_time = now_local - timedelta(days=now_local.weekday())
            start_time = start_time.replace(hour=0, minute=0, second=0, microsecond=0)
        elif timeFrame == "month":
            start_time = now_local.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        query = SUBMISSION_REF
        if start_time:
            query = query.where("submission_time", ">=", start_time)

        user_aggregates = {}

        for doc in query.stream():
            sub = doc.to_dict()
            student = sub.get("student", {})
            user_id = student.get("telegram_id")

            if not user_id:
                continue 

            time_taken_seconds = 0
            time_taken_raw = sub.get("time_spend", 0)
            if isinstance(time_taken_raw, str):
                try:
                    h, m, s = map(int, time_taken_raw.split(':'))
                    time_taken_seconds = h * 3600 + m * 60 + s
                except ValueError:
                    time_taken_seconds = 0

            elif isinstance(time_taken_raw, int):
                time_taken_seconds = time_taken_raw

            if user_id not in user_aggregates:
                user_aggregates[user_id] = {
                    "user_id": user_id,
                    "user_name": student.get("name", "Unknown"),
                    "score": sub.get("score", 0),
                    "correct_answers": sub.get("score", 0),
                    "total_questions": sub.get("score", 0) + len(sub.get("missed_questions", [])),
                    "time_taken": time_taken_seconds,
                    "imgurl": student.get("imgurl", ""),
                }
            else:
                user_aggregates[user_id]["score"] += sub.get("score", 0)
                user_aggregates[user_id]["correct_answers"] += sub.get("score", 0)
                user_aggregates[user_id]["total_questions"] += sub.get("score", 0) + len(sub.get("missed_questions", []))
                user_aggregates[user_id]["time_taken"] += time_taken_seconds

        leaderboard_list = list(user_aggregates.values())
        sorted_leaderboard = sorted(leaderboard_list, key=lambda u: (-u['score'], u['time_taken']))
        final_leaderboard = []
        for rank, entry in enumerate(sorted_leaderboard[:100], 1):
            entry["rank"] = rank
            entry["time_taken"] = LeaderboardRepository.format_seconds_to_hms(entry["time_taken"])
            final_leaderboard.append(entry)
        return final_leaderboard
