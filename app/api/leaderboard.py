from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Optional
from app.services.leaderboard_service import LeaderboardService

router = APIRouter()

@router.get("")
async def get_leaderboard(timeFrame: Optional[str] = Query("week", enum=["today", "week", "month", "all"])):
    try:
        leaderboard = await LeaderboardService.get_leaderboard(timeFrame)
        return JSONResponse({
            "leaderboard": leaderboard,
            "timeFrame": timeFrame,
            "status": "success"
        }, status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse({
            "message": str(e),
            "status": "error"
        }, status_code=500)