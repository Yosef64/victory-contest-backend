from app.repositories.statistics_repo import StatisticsRepository
from app.repositories.student_repo import StudentRepository # Import StudentRepository for ranking

class StatisticsService:
    @staticmethod
    async def get_user_statistics(student_id: str):
        """
        Fetches comprehensive statistics for a given student.
        """
        user_stats = StatisticsRepository.get_user_statistics(student_id)

        # Fetch student rankings using StudentRepository
        rankings = StudentRepository.get_student_rankings()

        # Find the student's rank
        rank = -1
        for inx, st in enumerate(rankings):
            if st["telegram_id"] == student_id:
                rank = inx + 1
                break

        user_stats["rank"] = rank
        return user_stats