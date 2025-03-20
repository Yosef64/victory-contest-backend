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
        return ContestRepository.get_number_of_participants(contest_id)
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
