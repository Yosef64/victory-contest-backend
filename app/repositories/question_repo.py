from app.db.firebase import QUESTION_REF,SUBMISSION_REF
from uuid import uuid4
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
            # Fetch all submissions for the student
            query = SUBMISSION_REF.where("student.telegram_id", "==", student_id)
            docs = query.stream()

            structured_data = {}

            for doc in docs:
                submission = doc.to_dict()
                missed_questions = submission.get("missed_question", [])

                for q in missed_questions:
                    grade = f"Grade_{q['grade']}"
                    subject = q["subject"]
                    chapter_key = f"Chapter_{q['chapter']}"

                    if grade not in structured_data:
                        structured_data[grade] = {}
                    if subject not in structured_data[grade]:
                        structured_data[grade][subject] = {}
                    if chapter_key not in structured_data[grade][subject]:
                        structured_data[grade][subject][chapter_key] = 0

                    structured_data[grade][subject][chapter_key] += 1

            return structured_data
        except Exception as e:
            print(f"🔥 Database error: {e}")
            return {}
