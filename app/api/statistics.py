from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.services.statistics_service import StatisticsService
from typing import Dict, Any

router = APIRouter()

@router.get("/{student_id}", response_model=Dict[str, Any])
async def get_statistics_for_student(student_id: str):
    """
    Fetches comprehensive statistics for a given student, including leaderboard data for the week.
    """
    try:
        stats = await StatisticsService.get_user_statistics(student_id)
        return stats # Return the stats directly
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))