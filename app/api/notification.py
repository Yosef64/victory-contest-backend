# app/api/notification.py
from fastapi import APIRouter, Depends, HTTPException
from app.services.notification_service import NotificationService
from app.auth.auth import get_current_user

router = APIRouter()

@router.get("/notification/{user_id}")
async def get_notifications(user_id: str):
    # Fetch direct notifications
    user_notifications = NotificationService.get_user_notifications(user_id)
    # Optionally, fetch group/broadcast notifications
    # For now, just return direct notifications
    return {"notifications": user_notifications}

@router.post("/notifications/mark-read")
async def mark_notifications_read(current_user: dict = Depends(get_current_user)):
    NotificationService.mark_as_read(current_user["id"])
    return {"status": "success"}

