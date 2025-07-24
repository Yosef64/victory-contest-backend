from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.services.statistics_service import StatisticsService
from typing import Dict, Any

router = APIRouter()

@router.get("/{student_id}", response_model=Dict[str, Any])
async def get_statistics_for_student(student_id: str):
    try:
        stats = await StatisticsService.get_user_statistics(student_id)
        return stats
    except Exception as e:
        # Return the error message in the response for debugging
        return JSONResponse(
            status_code=500,
            content={"detail": str(e)}
        )