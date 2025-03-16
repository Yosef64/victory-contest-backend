from app.db.firebase import db
from app.schemas.student import StudentCreate, StudentUpdate
from google.cloud.firestore import FieldFilter
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
        STUDENT_REF.document(student.telegram_id).set(student)
        return {"message": "Student added successfully"}
    @staticmethod
    def verify_student_paid(telegram_id):
        student = STUDENT_REF.document(telegram_id).get()
        return {"paid":student["paid"]}
    @staticmethod
    def get_paid_students():
        students = STUDENT_REF.where(filter=FieldFilter("paid","==",True))
        return students

    @staticmethod
    def get_students():
        """Fetches all student Telegram IDs from Firestore."""
        return [doc.to_dict() for doc in STUDENT_REF.stream()]

    @staticmethod
    def get_student_by_id(student_id: str):
        """Fetches a student by ID."""
        student_doc = STUDENT_REF.document(student_id).get()
        if not student_doc.exists:
            return None
        return student_doc.to_dict()
