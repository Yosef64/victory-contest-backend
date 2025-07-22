from app.repositories.submission_repo import SubmissionRepository
from app.schemas.submission import SubmissionSchema
from app.repositories.date import DateService
from google.cloud import firestore
class SubmissionService:
    @staticmethod
    def get_all_submissions():
        return SubmissionRepository.get_all_submissions()
    
    @staticmethod
    def get_for_week():
        start_time,end_time = DateService.get_week_range()
        return SubmissionRepository.get_by_range(start_time,end_time)
    
    @staticmethod
    def get_for_today():
        start_time,end_time = DateService.get_today_range()
        return SubmissionRepository.get_by_range(start_time,end_time)

    @staticmethod
    def get_for_month():
        start_time,end_time = DateService.get_month_range()
        return SubmissionRepository.get_by_range(start_time,end_time)
   
    @staticmethod
    def get_submissions_with_student_info():
        return SubmissionRepository.get_submissions_with_student_info()

    @staticmethod
    def get_grades_and_schools():
        return SubmissionRepository.get_all_submissions()
    
    @staticmethod
    def create_submission(submission):
        response = SubmissionRepository.save_submission(submission)

        return response
    @staticmethod
    def get_submissions_by_contest(contest_id):
        submission = SubmissionRepository.get_submissions_by_contest(contest_id)
        return submission
    @staticmethod
    def put_wrong_answers(user_id):
        SubmissionRepository.put_wrong_answers(user_id)
        return
        

