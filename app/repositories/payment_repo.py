from app.db.firebase import db
PAYMENT_REF = db.collection("payments")
class PaymentRepository:
    @staticmethod
    def add_payment(payment):
        """Adds a new payment to Firestore."""
        payment_id = payment["telegram_id"]
        PAYMENT_REF.document(payment_id).set(payment)
        return {"message": "Payment added successfully"}
    @staticmethod
    def update_payment(payment):
        """Updates an existing payment in Firestore."""
        telegram_id = payment["telegram_id"]
        PAYMENT_REF.document(telegram_id).set(payment)
        return {"message": "Payment updated successfully"}
    @staticmethod
    def get_payment_by_id(telegram_id: str):
        """Fetches a payment by Telegram ID."""
        payment_doc = PAYMENT_REF.document(telegram_id).get()
        if not payment_doc.exists:
            return {}
        return payment_doc.to_dict()
    @staticmethod
    def get_payments():
        """Fetches all payments from Firestore."""
        return {doc.id:doc.to_dict() for doc in PAYMENT_REF.stream()}