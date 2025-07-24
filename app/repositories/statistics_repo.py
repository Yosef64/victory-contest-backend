from app.db.firebase import db
from google.cloud.firestore import FieldFilter
from app.repositories.submission_repo import SUBMISSION_REF
from collections import defaultdict

STATISTICS_REF = db.collection("statistics")

def parse_time_spend(value):
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        if value.isdigit():
            return int(value)
        # Try to parse hh:mm:ss
        try:
            h, m, s = value.split(':')
            return int(h) * 3600 + int(m) * 60 + int(s)
        except Exception:
            return 0
    return 0

class StatisticsRepository:
    @staticmethod
    def get_user_statistics(student_id):
        submissions = SUBMISSION_REF.where(filter=FieldFilter("student.student_id","==",student_id)).stream()
        submissions = [submission.to_dict() for submission in submissions]

        total_contests = len(submissions)
        total_questions = sum(int(sub.get("total_questions", 0) or 0) for sub in submissions)
        correct_answers = sum(int(sub.get("score", 0) or 0) for sub in submissions)
        accuracy = int((correct_answers / total_questions) * 100) if total_questions else 0
        total_time = sum(parse_time_spend(sub.get("time_spend", 0)) for sub in submissions)
        average_time = int(total_time / total_questions) if total_questions else 0

        # Calculate subject, chapter, and grade statistics
        subject_stats = defaultdict(lambda: {"correct": 0, "total": 0, "accuracy": 0})
        chapter_stats = defaultdict(lambda: {"correct": 0, "total": 0, "accuracy": 0})
        grade_stats = defaultdict(lambda: {"correct": 0, "total": 0, "accuracy": 0})
        recommendations = [] # Placeholder for recommendations
        recent_activity = [] # Placeholder for recent activity

        for submission in submissions:
            questions = submission.get("questions", []) # Assuming questions are stored in submission
            for question in questions:
                subject = question.get("subject", "Unknown")
                chapter = question.get("chapter", "Unknown")
                grade = question.get("grade", "Unknown")
                is_correct = question.get("is_correct", False)

                # Update subject stats
                subject_stats[subject]["total"] += 1
                if is_correct:
                    subject_stats[subject]["correct"] += 1

                # Update chapter stats
                chapter_stats[chapter]["total"] += 1
                if is_correct:
                    chapter_stats[chapter]["correct"] += 1

                # Update grade stats
                grade_stats[grade]["total"] += 1
                if is_correct:
                    grade_stats[grade]["correct"] += 1
            # Add recent activity
            submission_time = submission.get("submission_time")
            score = submission.get("score", 0)
            recent_activity.append({"timestamp": submission_time, "score": score})

        # Calculate accuracy for subject, chapter, and grade
        for key in subject_stats:
            total = subject_stats[key]["total"]
            correct = subject_stats[key]["correct"]
            subject_stats[key]["accuracy"] = int((correct / total) * 100) if total else 0

        for key in chapter_stats:
            total = chapter_stats[key]["total"]
            correct = chapter_stats[key]["correct"]
            chapter_stats[key]["accuracy"] = int((correct / total) * 100) if total else 0

        for key in grade_stats:
            total = grade_stats[key]["total"]
            correct = grade_stats[key]["correct"]
            grade_stats[key]["accuracy"] = int((correct / total) * 100) if total else 0

        stats = {
            "total_contests": total_contests,
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "accuracy": accuracy,
            "average_time": average_time,
            "subjects": subject_stats,
            "chapters": chapter_stats,
            "grades": grade_stats,
            "recommendations": recommendations,
            "recent_activity": recent_activity,
            # 'leaderboard' is added in the service layer, not here
        }
        return stats