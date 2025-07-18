from app.db.firebase import db
from datetime import date, datetime, timedelta
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
    @staticmethod
    def get_payment_by_student_id(student_id: str):
        """Fetches a payment by student ID."""
        payment_doc = PAYMENT_REF.document(student_id).get()
        if not payment_doc.exists:
            return {}
        return payment_doc.to_dict()
    @staticmethod
    def calculate_next_payment_status(last_payment):
        """Calculates the next payment status based on the last payment."""
        if not last_payment:
            return {"paymentStatus":"unpaid","nextPayment":datetime.now().isoformat()}
        
        
        last_payment_date = last_payment.get("date")
        if not last_payment_date:
            return {"paymentStatus":"unpaid","nextPayment":datetime.now().isoformat()}
        
        last_payment_date = datetime.strptime(last_payment_date, "%Y-%m-%d")
        next_payment_due_date = last_payment_date + timedelta(days=30)
        
        if datetime.now() < next_payment_due_date:
            return {"paymentStatus":"active","nextPayment":next_payment_due_date.isoformat()}
        elif datetime.now() >= next_payment_due_date:
            return {"paymentStatus":"unpaid","nextPayment":next_payment_due_date.isoformat()}
        

