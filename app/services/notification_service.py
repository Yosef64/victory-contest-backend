# app/services/notification_service.py
from app.db.firebase import db
from datetime import datetime
from google.cloud import firestore

NOTIFICATION_REF = db.collection("notifications")

class NotificationService:
    @staticmethod
    def create_notification(user_id: str, message: str, notification_type: str):
        notification = {
            "userId": user_id,
            "message": message,
            "type": notification_type,
            "read": False,
            "createdAt": datetime.now()
        }
        NOTIFICATION_REF.add(notification)
        return notification

    @staticmethod
    def get_user_notifications(user_id: str, limit: int = 10):
        # Convert the stream to a list of dictionaries
        notifications_stream = (
            NOTIFICATION_REF.where("userId", "==", user_id)
            .order_by("createdAt", direction=firestore.Query.DESCENDING)
            .limit(limit)
            .stream()
        )
        notifications_list = []
        for doc in notifications_stream:
            notification_data = doc.to_dict()
            notification_data["id"] = doc.id  # Include document ID
            notifications_list.append(notification_data)
        return notifications_list

    @staticmethod
    def mark_as_read(user_id: str):
        unread_notifications = NOTIFICATION_REF.where("userId", "==", user_id).where("read", "==", False).stream()

        batch = db.batch()
        for notif in unread_notifications:
            notif_ref = NOTIFICATION_REF.document(notif.id)
            batch.update(notif_ref, {"read": True})

        batch.commit()
        return True