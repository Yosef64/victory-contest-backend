from app.repositories.question_repo import QuestionRepository

class QuestionService:
    @staticmethod
    def get_questions():
        return QuestionRepository.get_questions()

    @staticmethod
    def add_question(data):
        return QuestionRepository.add_question(data)

    @staticmethod
    def update_question(question_id, data):
        return QuestionRepository.update_question(question_id, data)

    @staticmethod
    def delete_question(question_id):
        return QuestionRepository.delete_question(question_id)
