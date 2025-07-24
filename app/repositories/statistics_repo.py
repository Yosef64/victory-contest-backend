from datetime import datetime, timedelta  # Added imports
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
        # Get all submissions for the student
        submissions = SUBMISSION_REF.where(
            filter=FieldFilter("student.telegram_id", "==", student_id)
        ).stream()
        
        submissions = [sub.to_dict() for sub in submissions]
        
        if not submissions:
            return {
                "total_contests": 0,
                "total_questions": 0,
                "correct_answers": 0,
                "accuracy": 0,
                "average_time": 0,
                "subjects": {},
                "chapters": {},
                "grades": {},
                "performance_trend": []
            }

        # Calculate basic stats
        total_contests = len(submissions)
        total_questions = sum(sub.get("total_questions", 0) for sub in submissions)
        correct_answers = sum(sub.get("correct_answers", 0) for sub in submissions)
        accuracy = round((correct_answers / total_questions) * 100, 2) if total_questions else 0
        
        # Calculate average time per question (convert hh:mm:ss to seconds if needed)
        total_time_seconds = 0
        for sub in submissions:
            time_spend = sub.get("time_spend", 0)
            if isinstance(time_spend, str):
                try:
                    h, m, s = map(int, time_spend.split(':'))
                    total_time_seconds += h * 3600 + m * 60 + s
                except:
                    pass
            else:
                total_time_seconds += time_spend
        
        average_time = round(total_time_seconds / total_questions, 2) if total_questions else 0

        # Calculate subject, chapter, and grade stats
        subject_stats = defaultdict(lambda: {"total": 0, "correct": 0, "accuracy": 0})
        chapter_stats = defaultdict(lambda: {"total": 0, "correct": 0, "accuracy": 0})
        grade_stats = defaultdict(lambda: {"total": 0, "correct": 0, "accuracy": 0})

        for submission in submissions:
            questions = submission.get("questions", [])
            for q in questions:
                subject = q.get("subject", "Unknown")
                chapter = q.get("chapter", "Unknown")
                grade = q.get("grade", "Unknown")
                is_correct = q.get("is_correct", False)

                subject_stats[subject]["total"] += 1
                chapter_stats[chapter]["total"] += 1
                grade_stats[grade]["total"] += 1

                if is_correct:
                    subject_stats[subject]["correct"] += 1
                    chapter_stats[chapter]["correct"] += 1
                    grade_stats[grade]["correct"] += 1

        # Calculate accuracy percentages
        for subject in subject_stats:
            total = subject_stats[subject]["total"]
            correct = subject_stats[subject]["correct"]
            subject_stats[subject]["accuracy"] = round((correct / total) * 100, 2) if total else 0

        for chapter in chapter_stats:
            total = chapter_stats[chapter]["total"]
            correct = chapter_stats[chapter]["correct"]
            chapter_stats[chapter]["accuracy"] = round((correct / total) * 100, 2) if total else 0

        for grade in grade_stats:
            total = grade_stats[grade]["total"]
            correct = grade_stats[grade]["correct"]
            grade_stats[grade]["accuracy"] = round((correct / total) * 100, 2) if total else 0

        # Create performance trend (last 6 months)
        performance_trend = []
        now = datetime.utcnow()
        for i in range(5, -1, -1):
            month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(days=30*i)
            month_end = (month_start + timedelta(days=30)).replace(hour=23, minute=59, second=59)
            
            month_submissions = [
                sub for sub in submissions 
                if month_start <= datetime.strptime(sub.get("submission_time"), "%Y-%m-%dT%H:%M:%S") <= month_end
            ]
            
            month_questions = sum(sub.get("total_questions", 0) for sub in month_submissions)
            month_correct = sum(sub.get("correct_answers", 0) for sub in month_submissions)
            month_accuracy = round((month_correct / month_questions) * 100, 2) if month_questions else 0
            
            performance_trend.append({
                "month": month_start.strftime("%b"),
                "accuracy": month_accuracy,
                "questions": month_questions
            })

        return {
            "total_contests": total_contests,
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "accuracy": accuracy,
            "average_time": average_time,
            "subjects": dict(subject_stats),
            "chapters": dict(chapter_stats),
            "grades": dict(grade_stats),
            "performance_trend": performance_trend
        }