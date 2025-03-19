from app.repositories.question_repo import QuestionRepository

class QuestionService:
    @staticmethod
    def get_questions():
        return QuestionRepository.get_questions()
    
    @staticmethod
    def add_questions(questions):
        return QuestionRepository.add_questions(questions)

    @staticmethod
    def add_question(data):
        return QuestionRepository.add_question(data)

    @staticmethod
    def update_question( data):
        return QuestionRepository.update_question(data)

    @staticmethod
    def delete_question(question_id):
        return QuestionRepository.delete_question(question_id)

    @staticmethod
    def get_missed_questions(student_id: str):
        return QuestionRepository.get_missed_questions(student_id)

    @staticmethod
    def get_weekly_missed_questions(student_id: str):
        return QuestionRepository.get_weekly_missed_questions(student_id)

    @staticmethod
    def get_monthly_missed_questions(student_id: str):
        return QuestionRepository.get_monthly_missed_questions(student_id) 
    

    @staticmethod
    def get_missed_questions_by_contest(contest_id: str, student_id: str):
        return QuestionRepository.get_submissions_by_contest_and_student(contest_id, student_id)

        