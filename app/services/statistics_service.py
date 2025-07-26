from app.repositories.statistics_repo import StatisticsRepository
from app.repositories.student_repo import StudentRepository # Import StudentRepository for ranking
from app.repositories.leaderboard_repo import LeaderboardRepository  # <-- Add this import

class StatisticsService:
    @staticmethod
    async def get_user_statistics(student_id: str):
        """
        Fetches comprehensive statistics for a given student.
        """
        user_stats = StatisticsRepository.get_user_stats(student_id)
        return user_stats