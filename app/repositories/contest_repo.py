from app.db.firebase import CONTEST_REF, SUBMISSION_REF, STUDENT_REF,REGISTERED__REF
from uuid import uuid4
from datetime import datetime, timezone
from app.repositories.question_repo import QuestionRepository
from google.cloud.firestore import FieldFilter

class ContestRepository:
    @staticmethod
    def get_all_contests():

        return [doc.to_dict() for doc in CONTEST_REF.stream()]
    
    def get_structured_contests():
        contests = ContestRepository.get_all_contests()
        structured_data = {}
        for contest in contests:
            structured_data[contest["id"]] = contest
        return structured_data
    
    @staticmethod
    def is_user_registered(contest_id: str, student_id: str):
        registration = REGISTERED__REF.where(filter=FieldFilter("contest_id", "==", contest_id)).where(filter=FieldFilter("student_id", "==", student_id)).get()
        return registration[0].exists if registration else False

    @staticmethod
    def get_contest_by_id(contest_id):
        ref = CONTEST_REF.document(contest_id).get()
        if not ref.exists:
            raise ValueError("Contest not found.")
        final_result = ref.to_dict() 
        if not final_result:
            return {}
        all_questions = QuestionRepository.get_structured_questions()
        if "questions" in final_result:
            final_result["questions"] = [all_questions[q_id] for q_id in final_result["questions"] if q_id in all_questions]
        else:
            final_result["questions"] = []

        return final_result
    @staticmethod   
    def get_participants(contest_id):
        registerations ,res = REGISTERED__REF.where("contest_id", "==", contest_id).stream(), []
        for doc in registerations:
            res.append(doc.to_dict())
        return res
                
    @staticmethod
    def get_active_contestants(contest_id):
        contest = REGISTERED__REF.document(contest_id).get()
        if not contest.exists:
            return []
        real_contest = contest.to_dict()
        if real_contest == None:
            return []
        
        return real_contest["active_contestant"]

    @staticmethod
    def add_contest(data):
        contest_id = str(uuid4()).replace("-", "")
        CONTEST_REF.document(contest_id).set({**data, "id": contest_id})
        return contest_id

    @staticmethod
    def update_contest(contest_id, data):
        CONTEST_REF.document(contest_id).update(data)
        return True

    @staticmethod
    def delete_contest(contest_id):
        CONTEST_REF.document(contest_id).delete()
        return True

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
    def get_active_contests():
        now = datetime.now(timezone.utc)
        active = []
        for doc in CONTEST_REF.stream():
            contest = doc.to_dict()
            try:
                end_date = datetime.fromisoformat(contest["end_date"].replace('Z', '+00:00'))
                if end_date > now:
                    active.append(contest)
            except Exception:
                continue
        return active

    @staticmethod
    def get_past_contests():
        now = datetime.now(timezone.utc)
        past = []
        for doc in CONTEST_REF.stream():
            contest = doc.to_dict()
            try:
                end_date = datetime.fromisoformat(contest["end_date"].replace('Z', '+00:00'))
                if end_date <= now:
                    past.append(contest)
            except Exception:
                continue
        return past
    @staticmethod
    def register_user_for_Contest(contest_id: str, student_id: str):
        reg_id = str(uuid4()).replace("-", "")
        REGISTERED__REF.document(reg_id).set({"id": reg_id,
  "contest_id": contest_id,
  "is_active":False, 
  "student_id": student_id,
  "registered_at": datetime.now(timezone.utc).isoformat(),})
        
        return True

    @staticmethod
    def activate_user(contest_id: str, student_id: str):
        registration = REGISTERED__REF.where("contest_id", "==", contest_id).where("student_id", "==", student_id).get()
        
        if not registration:
            raise ValueError("User is not registered for this contest.")

        reg_doc = registration[0]
        reg_data = reg_doc.to_dict() if hasattr(reg_doc, 'to_dict') else None

        if reg_data is None:
            raise ValueError("Invalid registration document.")

        if reg_data.get("is_active", False):
            raise ValueError("User is already active.")

        doc_ref = reg_doc.reference
        doc_ref.update({"is_active": True})
        
        return True

