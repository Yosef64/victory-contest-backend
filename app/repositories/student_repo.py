from starlette.background import P
from app.db.firebase import db
from app.schemas.student import StudentCreate, StudentUpdate
from google.cloud.firestore import FieldFilter
from app.repositories.submission_repo import SUBMISSION_REF, SubmissionRepository
from app.repositories.payment_repo import PaymentRepository
STUDENT_REF = db.collection("students")

class StudentRepository:
    @staticmethod
    def add_student(student):
        """Adds a new student to Firestore."""
        student_id = student["telegram_id"]
        STUDENT_REF.document(student_id).set(student)
        return {"message": "Student added successfully"}
    @staticmethod 
    def update_student(student):
        telegram_id = student["telegram_id"]
        STUDENT_REF.document(telegram_id).set(student)
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
    def get_quick_stat(student_id):
        submissions = SUBMISSION_REF.where(filter=FieldFilter("student.student_id","==",student_id)).stream()
        submissions = [submission.to_dict() for submission in submissions]
        total_time = sum(submission["time_spend"] for submission in submissions)
        total_points = sum(submission["score"] for submission in submissions)
        quick_stat = {"time": total_time,"contests": len(submissions),"points": total_points}
        return quick_stat

    @staticmethod
    def get_student_rankings():
        students = StudentRepository.get_students()
        submissions = SubmissionRepository.get_structured_submissions()
        rankings = []
        for student in students:
            student_id = student.get("telegram_id")
            stud_submission = submissions[student_id]
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
 
        grades = {"schools": set(), "grades": set()}
        for doc in STUDENT_REF.stream():
            student = doc.to_dict()
            if student.get("grade"):
                grades["grades"].add(student["grade"])
            if student.get("school"):
                grades["schools"].add(student["school"])
        return {"grades": list(grades["grades"]), "schools": list(grades["schools"])}
@staticmethod
def get_grades_and_schools():
    grades = {"schools": set(), "cities": set()}
    for doc in STUDENT_REF.stream():
        student = doc.to_dict()
        if student.get("school"):
            grades["schools"].add(student["school"])
        if student.get("city"):
            grades["cities"].add(student["city"])
    return {
        "schools": list(grades["schools"]), 
        "cities": list(grades["cities"])
    }


