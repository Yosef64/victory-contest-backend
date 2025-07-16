from app.repositories.contest_repo import ContestRepository

class ContestService:
    @staticmethod
    def get_all_contests():
        return ContestRepository.get_all_contests()

    @staticmethod
    def get_contest_by_id(contest_id):
        return ContestRepository.get_contest_by_id(contest_id)
    @staticmethod
    def get_number_of_participants(contest_id):
        return ContestRepository.get_participants(contest_id)
    
    @staticmethod
    def get_active_contestants(contest_id):
        return ContestRepository.get_active_contestants(contest_id)
    @staticmethod
    def register_contest(contest_id,student_id):
        return ContestRepository.register_contest(contest_id,student_id)

    @staticmethod
    def add_contest(data):
        return ContestRepository.add_contest(data)

    @staticmethod
    def update_contest(contest_id, data):
        return ContestRepository.update_contest(contest_id, data)

    @staticmethod
    def delete_contest(contest_id):
        return ContestRepository.delete_contest(contest_id)

    @staticmethod
    def get_all_submissions():
        return ContestRepository.get_all_submissions()

    @staticmethod
    def get_submissions_with_student_info():
        return ContestRepository.get_submissions_with_student_info()

    @staticmethod
    def get_grades_and_schools():
        return ContestRepository.get_grades_and_schools()

    @staticmethod
    def get_active_contests():
        return ContestRepository.get_active_contests()

    @staticmethod
    def get_past_contests():
        return ContestRepository.get_past_contests()
    @staticmethod
    def register_user_for_Contest(contest_id: str, student_id: str):
        return ContestRepository.register_user_for_Contest(contest_id, student_id)
    @staticmethod
    def is_user_registered(contest_id: str, student_id: str):
        return ContestRepository.is_user_registered(contest_id, student_id)
    
