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
        try:
            submission_data = submission.dict()
            
            response, status_code = SubmissionRepository.save_submission(submission_data)

            return response, status_code
        except Exception as e:
            print(f"🔥 Internal Server Error: {e}")  # Debugging
            return {"error": f"Internal server error: {str(e)}"}, 500

