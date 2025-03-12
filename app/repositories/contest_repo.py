from app.db.firebase import CONTEST_REF, SUBMISSION_REF, STUDENT_REF
from uuid import uuid4

class ContestRepository:
    @staticmethod
    def get_all_contests():
        return [doc.to_dict() for doc in CONTEST_REF.stream()]

    @staticmethod
    def get_contest_by_id(contest_id):
        ref = CONTEST_REF.document(contest_id).get()
        return ref.to_dict() if ref.exists else None

    @staticmethod
    def add_contest(data):
        contest_id = str(uuid4()).replace("-", "")
        CONTEST_REF.document(contest_id).set({**data, "active_contestant": [], "submissions": [], "contest_id": contest_id})
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
