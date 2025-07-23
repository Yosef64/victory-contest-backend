from datetime import datetime
from typing import List
from app.db.firebase import SUBMISSION_REF, STUDENT_REF,WRONG_ANSWER_REF
from google.cloud.firestore import FieldFilter
from uuid import uuid4
from app.repositories.date import DateService
from collections import defaultdict

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
    def save_submission(submission_data: dict):
        doc_ref = SUBMISSION_REF.document()  
        submission_data["submission_time"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        submission_data["submission_id"] = doc_ref.id 
        doc_ref.set(submission_data)
        
        return {"message": "success"}
       
    @staticmethod
    def get_submissions_by_contest(contest_id):
        docs = SUBMISSION_REF.where(filter=FieldFilter("contest_id", "==", contest_id)).stream()
        submissions = [doc.to_dict() for doc in docs]
        return submissions
    @staticmethod
    def put_wrong_answers(data):
        ref = WRONG_ANSWER_REF.document(data["user_id"])
        ref.update({})
    @staticmethod
    def get_user_submission(user_id):
        query = SUBMISSION_REF.where("student.telegram_id", "==", user_id)
        docs = query.stream()
        submissions = [doc.to_dict() for doc in docs]
        return submissions
    @staticmethod
    def get_structured_submissions():
        submissions = defaultdict(list)
        for doc in SUBMISSION_REF.stream():
            submission = doc.to_dict()
            student_data = submission.get("student", {})
            st_id = student_data.get("telegram_id")

            if st_id:
                submissions[st_id].append(submission)
            
        return submissions
    @staticmethod
    def get_structured_submissions_by_contest(contest_id:str):
        submissions = defaultdict(list)
        query = SUBMISSION_REF.where("contest.id", "==", contest_id)
        for doc in query.stream():
            submission = doc.to_dict()
            student_data = submission.get("student", {})
            st_id = student_data.get("telegram_id")
            if st_id:
                submissions[st_id].append(submission)
            
        return submissions
    @staticmethod
    def calculate_points(submissions:List[dict]) -> int:
        total_points = 0    

        for submission in submissions:
            total_points += submission["score"]
        return total_points
        
