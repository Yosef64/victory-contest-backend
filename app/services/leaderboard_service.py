from app.repositories.leaderboard_repo import LeaderboardRepository

class LeaderboardService:
    @staticmethod
    async def get_leaderboard(timeFrame: str = "week"):
        """
        Fetches the leaderboard data from the repository.
        """
        leaderboard = LeaderboardRepository.get_leaderboard(timeFrame)
        return leaderboard