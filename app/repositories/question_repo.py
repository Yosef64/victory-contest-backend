from app.db.firebase import QUESTION_REF
from uuid import uuid4

class QuestionRepository:
    @staticmethod
    def get_questions():
        return [doc.to_dict() for doc in QUESTION_REF.stream()]
    
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
