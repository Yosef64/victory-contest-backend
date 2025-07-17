# app/services/notification_service.py
from app.db.firebase import db
from datetime import datetime
from google.cloud import firestore

NOTIFICATIONS_REF = db.collection("notifications")
STUDENT_NOTIFICATIONS_REF = db.collection("student_notifications")  # for flat structure


class NotificationService:
    @staticmethod
    def create_group_notification(message: str, notification_type: str, student_ids: list,title:str):
        """
        Create a shared notification and link it to many students.
        """
        # Step 1: Create shared notification
        notification = {
            "title":title,
            "message": message,
            "type": notification_type,
            "sent_at": datetime.utcnow(),
        }
        notif_ref = NOTIFICATIONS_REF.document()
        notif_ref.set(notification)

        # Step 2: Link to all students
        batch = db.batch()
        for student_id in student_ids:
            doc_ref = STUDENT_NOTIFICATIONS_REF.document()
            batch.set(doc_ref, {
                "notification_id": notif_ref.id,
                "recipient_id": student_id,
                "is_read": False
            })
        batch.commit()
        return {"notification_id": notif_ref.id, "recipients": student_ids}

    @staticmethod
    def create_personal_notification(student_id: str, message: str, notification_type: str,title:str):
        """
        Create a notification for a single user.
        """
        notification = {
            "title":title,
            "message": message,
            "type": notification_type,
            "sent_at": datetime.utcnow()
        }
        notif_ref = NOTIFICATIONS_REF.document()
        notif_ref.set(notification)

        # Link it to that student
        student_notif_ref = STUDENT_NOTIFICATIONS_REF.document()
        student_notif_ref.set({
            "notification_id": notif_ref.id,
            "recipient_id": student_id,
            "is_read": False
        })
        return {"notification_id": notif_ref.id, "recipient": student_id}

    @staticmethod
    def get_user_notifications(student_id: str, limit: int = 10):
        """
        Return a list of notifications for a student (joined from both collections).
        """
        notif_links = STUDENT_NOTIFICATIONS_REF \
            .where("recipient_id", "==", student_id) \
            .order_by("is_read") \
            .limit(limit) \
            .stream()

        notifications = []
        for doc in notif_links:
            data = doc.to_dict()
            notif_id = data.get("notification_id")
            notif_doc = NOTIFICATIONS_REF.document(notif_id).get()
            if notif_doc.exists:
                notif_data = notif_doc.to_dict()
                if notif_data:
                    notif_data["id"] = notif_doc.id
                    notif_data["is_read"] = data.get("is_read", False)
                notifications.append(notif_data)
        return notifications

    @staticmethod
    def mark_as_read(student_id: str):
        """
        Mark all notifications for a student as read.
        """
        unread_refs = STUDENT_NOTIFICATIONS_REF \
            .where("recipient_id", "==", student_id) \
            .where("is_read", "==", False) \
            .stream()

        batch = db.batch()
        for doc in unread_refs:
            ref = STUDENT_NOTIFICATIONS_REF.document(doc.id)
            batch.update(ref, {"is_read": True})
        batch.commit()
        return True
