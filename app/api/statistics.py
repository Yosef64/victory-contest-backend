from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.services.statistics_service import StatisticsService
from typing import Dict, Any

router = APIRouter()

@router.get("/{student_id}")
async def get_statistics_for_student(student_id: str):
    try:
        stats = await StatisticsService.get_user_statistics(student_id)
        return JSONResponse({
            "status": "success",
            "data": stats
        }, status_code=200)
    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": str(e)
        }, status_code=500)