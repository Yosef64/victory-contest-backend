from app.repositories.submission_repo import SubmissionRepository
from app.schemas.submission import SubmissionSchema
class SubmissionService:
    @staticmethod
    def get_all_submissions():
        return SubmissionRepository.get_all_submissions()
   
    @staticmethod
    def get_submissions_with_student_info():
        return SubmissionRepository.get_submissions_with_student_info()

    @staticmethod
    def get_grades_and_schools():
        return SubmissionRepository.get_grades_and_schools()
    
    @staticmethod
    def create_submission(submission: SubmissionSchema):
       
        submission_data = submission.dict()
        
        response, status_code = SubmissionRepository.save_submission(submission_data)

        return response, status_code
    @staticmethod
    def get_submissions_by_contest(contest_id):
        submission = SubmissionRepository.get_submissions_by_contest(contest_id)
        return submission
    @staticmethod
    def put_wrong_answers(user_id):
        SubmissionRepository.put_wrong_answers(user_id)
        return
        

