from app.db.firebase import QUESTION_REF,SUBMISSION_REF
from uuid import uuid4
from datetime import datetime, timedelta
import pytz
from google.cloud import firestore

class QuestionRepository:
    @staticmethod
    def get_questions():
        return [
    doc.to_dict() if "id" in doc.to_dict() else {**doc.to_dict(), "id": doc.id} 
    for doc in QUESTION_REF.stream()]
    
    @staticmethod
    def add_questions(questions):
        for question in questions:
            QuestionRepository.add_question(question)
        return True

    @staticmethod
    def add_question(data):
        question_id = str(uuid4()).replace("-", "")
        QUESTION_REF.document(question_id).set({**data,"id":question_id})
        return question_id

    @staticmethod
    def update_question(data):
        QUESTION_REF.document(data.id).update(data)
        return True

    @staticmethod
    def delete_question(question_id):
        QUESTION_REF.document(question_id).delete()
        return True


    @staticmethod
    def get_missed_questions(student_id: str):
        try:
            # Use 'filter=' in 'where()' to prevent warnings
            query = SUBMISSION_REF.where("student.Student_id", "==", student_id)
            docs = list(query.stream())

            if not docs:
                print(f"No submissions found for student_id: {student_id}")
                return {"missed_questions": {}}

            structured_data = {}

            for doc in docs:
                submission = doc.to_dict()
                missed_questions = submission.get("missed_question", [])

                for q in missed_questions:
                    grade = f"Grade_{q['grade']}"
                    subject = q["subject"]
                    chapter_key = f"Chapter_{q['chapter']}"

                    # Use setdefault() for cleaner nested dictionary initialization
                    structured_data.setdefault(grade, {}).setdefault(subject, {}).setdefault(chapter_key, 0)

                    # Increment missed question count
                    structured_data[grade][subject][chapter_key] += 1

            return structured_data

        except Exception as e:
            print(f"🔥 Database error: {e}")
            return {"missed_questions": {}}




    @staticmethod
    def get_weekly_missed_questions(student_id: str):
        try:
            # Get the current time in UTC
            now = datetime.utcnow()

            # Calculate the most recent Monday
            days_since_monday = now.weekday()  # Monday = 0, Sunday = 6
            most_recent_monday = now - timedelta(days=days_since_monday)
            most_recent_monday = most_recent_monday.replace(hour=0, minute=0, second=0, microsecond=0)

            # Convert to Firestore timestamp format
            firestore_monday = most_recent_monday.astimezone(pytz.utc)

            # Fetch submissions from the current week
            query = (
                            SUBMISSION_REF
                            .where(filter=firestore.FieldFilter("student.Student_id", "==", student_id))
                            .where(filter=firestore.FieldFilter("submission_time", ">=", firestore_monday))
                        )
            docs = list(query.stream())

            if not docs:
                print(f"No weekly submissions found for student_id: {student_id}")
                return {"missed_questions": {}}

            structured_data = {}

            for doc in docs:
                submission = doc.to_dict()
                missed_questions = submission.get("missed_question", [])

                for q in missed_questions:
                    grade = f"Grade_{q['grade']}"
                    subject = q["subject"]
                    chapter_key = f"Chapter_{q['chapter']}"

                    # Use setdefault() for cleaner nested dictionary initialization
                    structured_data.setdefault(grade, {}).setdefault(subject, {}).setdefault(chapter_key, 0)

                    # Increment missed question count
                    structured_data[grade][subject][chapter_key] += 1

            return structured_data

        except Exception as e:
            print(f"🔥 Database error: {e}")
            return {"missed_questions": {}}
        

    @staticmethod
    def get_monthly_missed_questions(student_id: str):
        try:
            # Get current time in UTC
            now = datetime.utcnow()
            
            # Get the first day of the current month at midnight
            first_day_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            
            # Convert to Firestore timestamp format
            firestore_first_day = first_day_of_month.astimezone(pytz.utc)

            # Fetch submissions from the current month
            query = (
                SUBMISSION_REF
                .where(filter=firestore.FieldFilter("student.Student_id", "==", student_id))
                .where(filter=firestore.FieldFilter("submission_time", ">=", firestore_first_day))
            )
            docs = query.stream()

            structured_data = {}

            for doc in docs:
                submission = doc.to_dict()
                missed_questions = submission.get("missed_question", [])

                for q in missed_questions:
                    grade = f"Grade_{q['grade']}"
                    subject = q["subject"]
                    chapter_key = f"Chapter_{q['chapter']}"

                    # Use setdefault for cleaner nested dictionary initialization
                    structured_data.setdefault(grade, {}).setdefault(subject, {}).setdefault(chapter_key, 0)
                    structured_data[grade][subject][chapter_key] += 1

            return structured_data

        except Exception as e:
            print(f"🔥 Database error: {e}")
            return {}
        

    @staticmethod
    def get_submissions_by_contest_and_student(contest_id: str, student_id: str):
        try:
            # Fetch the submission for the given contest and student
            query = (
                SUBMISSION_REF
                .where(filter=firestore.FieldFilter("contest_id", "==", contest_id))
                .where(filter=firestore.FieldFilter("student.Student_id", "==", student_id))
            )
            docs = list(query.stream())

            # If no submission is found, return an empty dictionary
            if not docs:
                print(f"No submission found for contest_id: {contest_id} and student_id: {student_id}")
                return {}

            # Get the first (and only) submission
            submission = docs[0].to_dict()
            missed_questions = submission.get("missed_question", [])

            structured_data = {}

            # Process missed questions
            for q in missed_questions:
                grade = f"Grade_{q['grade']}"
                subject = q["subject"]
                chapter_key = f"Chapter_{q['chapter']}"

                # Use setdefault for cleaner nested dictionary initialization
                structured_data.setdefault(grade, {}).setdefault(subject, {}).setdefault(chapter_key, 0)
                structured_data[grade][subject][chapter_key] += 1

            return structured_data

        except Exception as e:
            # Log the error for debugging purposes
            print(f"🔥 Database error: {e}")
            return {}