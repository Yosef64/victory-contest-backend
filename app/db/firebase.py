import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate("app/db/key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
QUESTION_REF = db.collection("questions")
CONTEST_REF = db.collection("contests")
SUBMISSION_REF = db.collection("submissions")
STUDENT_REF = db.collection("students")
