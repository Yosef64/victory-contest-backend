# app/api/notifications.py
from fastapi import APIRouter, Depends, HTTPException
from app.services.notification_service import NotificationService
from app.auth.auth import get_current_user

router = APIRouter()

@router.get("/notifications")
async def get_notifications(current_user: dict = Depends(get_current_user)):
    notifications = NotificationService.get_user_notifications(current_user["id"])
    return [notif.to_dict() for notif in notifications]

@router.post("/notifications/mark-read")
async def mark_notifications_read(current_user: dict = Depends(get_current_user)):
    NotificationService.mark_as_read(current_user["id"])
    return {"status": "success"}

# app/api/search.py
from fastapi import APIRouter, HTTPException
from app.services.search_service import SearchService

router = APIRouter()

@router.get("/search")
async def search_menu_items(query: str):
    if not query or len(query) < 2:
        raise HTTPException(status_code=400, detail="Query must be at least 2 characters")
    return SearchService.search_menu_items(query)