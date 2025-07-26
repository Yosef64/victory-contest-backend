from datetime import datetime, timedelta  # Added imports
from app.db.firebase import db
from google.cloud.firestore import FieldFilter
from app.repositories.submission_repo import SUBMISSION_REF
from collections import defaultdict
from app.repositories.submission_repo import SubmissionRepository
from app.repositories.question_repo import QuestionRepository
from app.repositories.contest_repo import ContestRepository
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
    def get_user_stats(student_id: str) -> dict:
        user_submissions = SubmissionRepository.get_user_submission(student_id)
        all_questions = QuestionRepository.get_structured_questions()
        all_contests = ContestRepository.get_structured_contests()

        if not user_submissions:
            return {
                "total_contests": 0, "total_questions": 0, "correct_answers": 0,
                "accuracy": 0.0, "average_time": 0.0, "subjects": {},
                "chapters": {}, "grades": {}, "performance_trend": [],
            }

        contests_participated = set()
        total_time_seconds = 0
        subjects = defaultdict(lambda: {"total": 0, "correct": 0})
        chapters = defaultdict(lambda: {"total": 0, "correct": 0})
        grades = defaultdict(lambda: {"total": 0, "correct": 0})
        performance_trend = defaultdict(lambda: {"total": 0, "correct": 0})

        for sub in user_submissions:
            contest = all_contests.get(sub['contest_id'])
            if not contest:
                continue

            contests_participated.add(contest['id'])

            try:
                h, m, s = map(int, sub['time_spend'].split(':'))
                total_time_seconds += h * 3600 + m * 60 + s
            except (ValueError, AttributeError):
                pass

            missed_question_ids = set(sub['missed_questions'])

            try:
                submission_dt_object = datetime.fromisoformat(sub['submission_time'].replace('Z', '+00:00'))
                submission_month = submission_dt_object.strftime('%Y-%m')
            except (TypeError, ValueError):
                submission_month = "unknown-month"

            for question_id in contest['questions']:
                question = all_questions.get(question_id)
                if not question:
                    continue

                is_correct = question_id not in missed_question_ids

                subjects[question['subject']]['total'] += 1
                chapters[question['chapter']]['total'] += 1
                grades[question['grade']]['total'] += 1
                performance_trend[submission_month]['total'] += 1
                if is_correct:
                    subjects[question['subject']]['correct'] += 1
                    chapters[question['chapter']]['correct'] += 1
                    grades[question['grade']]['correct'] += 1
                    performance_trend[submission_month]['correct'] += 1

        # ... (Final calculation and return logic is the same)
        total_contests_val = len(contests_participated)
        total_questions_val = sum(cat['total'] for cat in subjects.values())
        correct_answers_val = sum(cat['correct'] for cat in subjects.values())

        accuracy_val = (correct_answers_val / total_questions_val * 100) if total_questions_val > 0 else 0.0
        average_time_val = total_time_seconds / total_contests_val if total_contests_val > 0 else 0.0

        for category_data in [subjects, chapters, grades]:
            for value in category_data.values():
                value['accuracy'] = round((value['correct'] / value['total'] * 100), 2) if value['total'] > 0 else 0.0

        trend_list = []
        for month, data in sorted(performance_trend.items()):
            trend_list.append({
                "month": month,
                "accuracy": round((data['correct'] / data['total'] * 100), 2) if data['total'] > 0 else 0.0,
                "questions": data['total']
            })

        return {
            "total_contests": total_contests_val, "total_questions": total_questions_val,
            "correct_answers": correct_answers_val, "accuracy": round(accuracy_val, 2),
            "average_time": round(average_time_val, 2), "subjects": dict(subjects),
            "chapters": dict(chapters), "grades": dict(grades),
            "performance_trend": trend_list
        }