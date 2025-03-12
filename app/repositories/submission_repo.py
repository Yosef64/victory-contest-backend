from app.db.firebase import SUBMISSION_REF, STUDENT_REF
from uuid import uuid4

class SubmissionRepository:
    @staticmethod
    def get_all_submissions():
        return [doc.to_dict() for doc in SUBMISSION_REF.stream()]

    @staticmethod
    def get_submissions_with_student_info():
        students = {stud.id: stud.to_dict() for stud in STUDENT_REF.stream()}
        submissions = []
        for doc in SUBMISSION_REF.stream():
            submission = doc.to_dict()
            student = students.get(submission.get("student_id"))
            if student:
                submissions.append({**student, **submission})
        return submissions

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
    def save_submission(submission_data: dict):
        try:
            # Generate a unique submission ID using Firestore
            doc_ref = SUBMISSION_REF.document()  # Auto-generates a unique ID
            submission_data["submission_id"] = doc_ref.id  # Add generated ID to data
            
            doc_ref.set(submission_data)
            
            return {"message": "Submission created successfully", "submission_id": doc_ref.id}, 201
        except Exception as e:
            print(f"🔥 Firestore error: {e}")  # Debugging
            return {"error": f"Database error: {str(e)}"}, 500