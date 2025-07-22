from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Optional
from app.services.leaderboard_service import LeaderboardService

router = APIRouter()

@router.get("/", response_model=dict)
async def get_leaderboard(timeFrame: Optional[str] = Query(None, enum=["today", "week", "month", "all"])):
    """
    Fetches the leaderboard data based on the specified time frame.
    """
    try:
        leaderboard = await LeaderboardService.get_leaderboard(timeFrame)
        return JSONResponse({"leaderboard": leaderboard}, status_code=200)
    except Exception as e:
        return JSONResponse({"message": str(e)}, status_code=500)