import datetime
from app.db.firebase import STUDENT_REF
achievements = [
    {
        "id":"1",
      "name": "First Steps",
      "description": "Complete your first contest",
      "type": "first",
      "rarity": "common",
      "earned": False,
      "earnedDate": "2024-01-10",
    },
    {
        "id": "2",
      "name": "Speed Demon",
      "description": "Answer 10 questions in under 30 seconds",
      "type": "speed",
      "rarity": "rare",
      "earned": False,
      "earnedDate": "",
    },
    {
        "id": "3",
      "name": "Perfectionist",
      "description": "Score 100% in any contest",
      "type": "perfection",
      "rarity": "epic",
      "earned": False,
    },
    {
        "id": "4",
      "name": "Streak Master",
      "description": "Maintain a 7-day winning streak",
      "type": "streak",
      "rarity": "rare",
      "earned": False,
      "earnedDate": "2024-01-20",
    },
    {
        "id": "5",
      "name": "Math Wizard",
      "description": "Score 90%+ in 5 math contests",
      "type": "subject",
      "rarity": "epic",
      "earned": False,
      "earnedDate": "",
    },
    {
        "id": "6",
      "name": "Champion",
      "description": "Reach top 10 in global leaderboard",
      "type": "rank",
      "rarity": "legendary",
      "earned": False,
    },
  ];


class BadgeRepository:
    @staticmethod
    def get_user_badges(student_id: str):
        """
        Fetches badges for a specific student.
        """
        student_doc = STUDENT_REF.document(student_id).get()
        if not student_doc.exists:
            return []
        student_data = student_doc.to_dict()
        if student_data is None:
            return []
        stud_achi = set(student_data.get("achievements", []))
        if not achievements:
            return []
        # Filter out only the earned badges
        badges = achievements.copy()
        for badge in stud_achi:
            if badge["id"] in stud_achi:
                badges[badge["id"]]["earned"] = True
                badges[badge["id"]]["earnedDate"] = datetime.datetime.now().strftime("%Y-%m-%d")
        return badges

