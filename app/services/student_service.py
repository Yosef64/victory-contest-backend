from app.repositories.student_repo import StudentRepository
from app.schemas.student import StudentCreate, StudentUpdate

class StudentService:
    @staticmethod
    def add_student(student):
        StudentRepository.add_student(student)
    
    @staticmethod
    def update_student(student):
        message = StudentRepository.update_student(student)
        return message
    @staticmethod
    def verify_student_paid(telegram_id):
        message = StudentRepository.verify_student_paid(telegram_id)
        return message
    @staticmethod
    def get_paid_students():
        student = StudentRepository.get_paid_students()
        return student

    
    @staticmethod
    def get_students():
        return StudentRepository.get_students()

    @staticmethod
    def get_student_by_id(student_id: str):
        return StudentRepository.get_student_by_id(student_id)
    @staticmethod
    def get_quick_stat(student_id):
        return StudentRepository.get_quick_stat(student_id)
    @staticmethod
    def get_student_rankings():
        return StudentRepository.get_student_rankings()

    @staticmethod
    def get_student_rankings_by_contest(contest_id: str):
        return StudentRepository.get_student_rankings_by_contest(contest_id)

    @staticmethod
    def get_user_profile(student_id: str):
        return StudentRepository.get_user_profile(student_id)
    @staticmethod
    def get_student_editorial(student_id: str,contest_id:str):
        return StudentRepository.get_student_editorial(student_id,contest_id)
