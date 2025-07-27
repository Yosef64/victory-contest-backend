from fastapi import Query
from starlette.background import P
from app.db.firebase import CONTEST_REF, QUESTION_REF, db
from app.schemas.student import StudentCreate, StudentUpdate
from google.cloud.firestore import FieldFilter
from app.repositories.submission_repo import SUBMISSION_REF, SubmissionRepository
from app.repositories.payment_repo import PaymentRepository
from app.repositories.contest_repo import ContestRepository
STUDENT_REF = db.collection("students")

class StudentRepository:
    @staticmethod
    def _time_str_to_seconds(time_str):
        """Converts a 'hh:mm:ss' string to total seconds."""
        if not isinstance(time_str, str):
            return 0
        try:
            parts = time_str.split(':')
            if len(parts) != 3:
                return 0
            
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = int(parts[2])
            return hours * 3600 + minutes * 60 + seconds
        except (ValueError, IndexError):
            return 0
    @staticmethod
    def add_student(student):
        """Adds a new student to Firestore."""
        student_id = student["telegram_id"]
        STUDENT_REF.document(student_id).set(student)
        return {"message": "Student added successfully"}
    @staticmethod 
    def update_student(student):
        telegram_id = student["telegram_id"]
        STUDENT_REF.document(telegram_id).update(student)
        return {"message": "Student added successfully"}
    @staticmethod
    def verify_student_paid(telegram_id):
        student = STUDENT_REF.document(telegram_id).get()
        if student.exists:
            st = student.to_dict()
            return {"paid":st["paid"] if st else False}
        return {"paid":False}
    @staticmethod
    def get_paid_students():
        students = STUDENT_REF.where(filter=FieldFilter("paid","==",True))
        return students

    @staticmethod
    def get_students():
        """Fetches all student Telegram IDs from Firestore."""
        payments = PaymentRepository.get_payments()
        students = []
        for doc in STUDENT_REF.stream():
            student_data = doc.to_dict()
            student_data["telegram_id"] = doc.id
            student_data["payment"] = payments.get(doc.id, None)
            students.append(student_data)
        return students

    @staticmethod
    def get_student_by_id(student_id: str):
        """Fetches a student by ID."""
        student_doc = STUDENT_REF.document(student_id).get()
        if not student_doc.exists:
            return {}
        return student_doc.to_dict()
    @staticmethod
    def get_user_statistics(telegram_id):
        submissions = SUBMISSION_REF.where(
        filter=FieldFilter("student.telegram_id", "==", telegram_id)).stream()
        submissions = [submission.to_dict() for submission in submissions]
        total_contests = len(submissions)
        total_questions = sum(len(sub.get("missed_questions", [])) + sub.get("score",0) for sub in submissions)
        correct_answers = sum(sub.get("score", 0) for sub in submissions)
        accuracy = int((correct_answers / total_questions) * 100) if total_questions else 0
        total_time = sum(StudentRepository._time_str_to_seconds(sub.get("time_spend")) for sub in submissions)
        average_time = int(total_time / total_questions) if total_questions else 0
        rankings = StudentRepository.get_student_rankings()
        rank = -1
        for inx, st in enumerate(rankings):
            if st["telegram_id"] == telegram_id:
                rank = inx + 1
                break
        
        # Streak calculation can be added if you have submission dates
        stats = {
            "totalContests": total_contests,
            "totalQuestions": total_questions,
            "correctAnswers": correct_answers,
            "accuracy": accuracy,
            "averageTime": average_time,
            "rank": rank
            # "streak": streak, # Add streak logic if available
        }
        return stats

    @staticmethod
    def get_student_rankings():
        students = StudentRepository.get_students()
        submissions = SubmissionRepository.get_structured_submissions()
        rankings = []
        for student in students:
            student_id = student.get("telegram_id")
            stud_submission = submissions.get(student_id, [])
            total_points = SubmissionRepository.calculate_points(stud_submission)
            rankings.append({
                "telegram_id": student_id,
                "name": student.get("name"),
                "total_points": total_points
            })
        # Sort by total_points descending
        rankings.sort(key=lambda x: x["total_points"], reverse=True)
        # Add rank
        for idx, student in enumerate(rankings, start=1):
            student["rank"] = idx
        return rankings
    @staticmethod
    def get_quick_stat(student_id: str):
        """Fetches quick statistics for a student."""
        student = STUDENT_REF.document(student_id).get()
        if not student.exists:
            raise ValueError("No student found with the provided ID.")
        student_data = student.to_dict()
        total_user_submissions = SubmissionRepository.get_user_submission(student_id)
        total_points = SubmissionRepository.calculate_points(total_user_submissions)
        payment = PaymentRepository.get_payment_by_student_id(student_id) or {}
        payment_date = payment.get("payment_date", "")
        pay_stat_next = PaymentRepository.calculate_next_payment_status(payment) or {}
        payment_to_result = {"lastPayment": payment_date, **pay_stat_next}
        if not student_data:
            raise ValueError("No student data found.")
        result = {
            "telegram_id": student_data.get("telegram_id"),
            "name": student_data.get("name"),
            "totalPoints": total_points,
            "payment": payment_to_result,
            "contestSubmissions": total_user_submissions
        }
        return result
 
    @staticmethod
    def get_student_rankings_by_contest(contest_id: str):
        
        submissions = SubmissionRepository.get_structured_submissions_by_contest(contest_id)
        rankings = []
        for student_submissions in submissions.values():
            if not student_submissions:
                continue
            sub = student_submissions[0]
            
            student = sub.get("student")
            if not student:
                continue

            rankings.append({
                "user_id": student.get("id", student.get("telegram_id")),
                "user_name": student.get("name"),
                "score": sub.get("score", 0),
                "correct_answers": sub.get("score", 0),
                "total_questions": len(sub.get("missed_questions", [])) + sub.get("score", 0),
                "time_taken": sub.get("time_spend", 0),
            })
            
        rankings.sort(key=lambda x: (-x["score"], x["time_taken"]))
        
        for idx, student_rank_data in enumerate(rankings, start=1):
            student_rank_data["rank"] = idx
            
        return rankings
    @staticmethod
    def get_grades_and_schools():
        grades = {"schools": set(), "grades": set()}
        for doc in STUDENT_REF.stream():
            student = doc.to_dict()
            if student.get("grade"):
                grades["grades"].add(student["grade"])
            if student.get("school"):
                grades["schools"].add(student["school"])
        return {"grades": list(grades["grades"]), "schools": list(grades["schools"])}
    
    @staticmethod
    def get_user_profile(student_id: str = ""):
        # Return the first student in the collection, or a default if none exist
        docs = STUDENT_REF.document(student_id).get()
        if not docs.exists:
            raise ValueError("No student found with the provided ID.")
        student = docs.to_dict() or {}
        total_user_submissions = SubmissionRepository.get_user_submission(docs.id)
        total_points = SubmissionRepository.calculate_points(total_user_submissions)
        payment = PaymentRepository.get_payment_by_student_id(docs.id) or {} 
        payment_date = payment.get("payment_date","")
        pay_stat_next = PaymentRepository.calculate_next_payment_status(payment) or {}
        payment_to_result = {"lastPayment":payment_date,**pay_stat_next}
        contest_submissions = []
        for inx, sub in enumerate(total_user_submissions):
            contest = sub.get("contest", {})
            if contest:
                contest_submissions.append({
                    "id": sub.get("id",inx+1),
                    "contest": {
                        "id": contest.get("id"),
                        "title": contest.get("title"),
                        "subject": contest.get("subject"),
                        "grade": contest.get("grade")
                    },
                    "totalQuestions": len(sub.get("missed_questions", [])) + sub.get("score", 0),
                    "correctAnswers": sub.get("score", 0),
                    "missedQuestions": len(sub.get("missed_questions", [])),
                    "score": sub.get("score", 0),
                    "submittedAt": sub.get("submitted_at", None)
                })

        result = {**student}
        result["totalPoints"] = total_points
        result["payment"] = payment_to_result
        result["contestSubmissions"] = contest_submissions
        return result
    def get_student_editorial(student_id: str, contest_id: str):
        """
        Fetches the editorial for a student's submission in a specific contest.
        This version is optimized for performance and better error handling.
        """
        
        submission = SubmissionRepository.get_submission_by_student_and_contest(student_id, contest_id)
        contest = ContestRepository.get_contest_by_id(contest_id)
        questions = contest.get("questions", [])
        missed_questions_list = submission.get("missed_questions", [])
        print(missed_questions_list)
        missed_questions_map = {
            missed.get("id"): missed
            for missed in missed_questions_list
        }
        print(missed_questions_map)

        editorial = []

        for question in questions:
            question_id = question.get("id")            
            if question_id in missed_questions_map:
                missed_info = missed_questions_map[question_id]
                question["is_correct"] = False
                question["user_answer"] = int(missed_info.get("selected_answer", -1)) 
            else:
                missed_info = missed_questions_map[question_id] if question_id in missed_questions_map else None
                question["is_correct"] = None if not submission else  True
                question["user_answer"] = missed_info["selected_answer"] if missed_info else None

            editorial.append(question)
                
        return editorial