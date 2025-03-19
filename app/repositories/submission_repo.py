from datetime import datetime
from app.db.firebase import SUBMISSION_REF, STUDENT_REF,WRONG_ANSWER_REF
from google.cloud.firestore import FieldFilter
from uuid import uuid4
from app.repositories.date import DateService

class SubmissionRepository:
    @staticmethod
    def get_all_submissions():
        return [doc.to_dict() for doc in SUBMISSION_REF.stream()]
    
    @staticmethod
    def get_by_range(start_time,end_time):

        query = SUBMISSION_REF.where("submission_time", ">=", start_time)\
                            .where("submission_time", "<=", end_time)
        docs = query.stream()

        submissions = []
        for doc in docs:
            submissions.append({"id": doc.id, **doc.to_dict()})

        return submissions

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
     
        doc_ref = SUBMISSION_REF.document()  
        submission_data["submission_time"] = datetime.utcnow()
        submission_data["submission_id"] = doc_ref.id 
        doc_ref.set(submission_data)
        
        return {"message": "success"}
       
    @staticmethod
    def get_submissions_by_contest(contest_id):
        docs = SUBMISSION_REF.where(filter=FieldFilter("contest_id", "==", contest_id)).stream()
        submissions = [doc.to_dict() for doc in docs]
        print(submissions)
        return submissions
    @staticmethod
    def put_wrong_answers(data):
        ref = WRONG_ANSWER_REF.document(data["user_id"])
        ref.update({})
        
