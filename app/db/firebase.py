import os
import base64
import json
import firebase_admin
from firebase_admin import credentials, firestore

base64_key = os.getenv("FIREBASE_CREDENTIALS")

if not base64_key:
    raise ValueError("FIREBASE_CREDENTIALS environment variable not set.")

try:
    firebase_key_json = json.loads(base64.b64decode(base64_key).decode('utf-8'))
    cred = credentials.Certificate(firebase_key_json)
except (json.JSONDecodeError, base64.binascii.Error) as e:
    raise ValueError(f"Invalid FIREBASE_CREDENTIALS: {e}")

firebase_admin.initialize_app(cred)

db = firestore.client()
QUESTION_REF = db.collection("questions")
CONTEST_REF = db.collection("contests")
SUBMISSION_REF = db.collection("submissions")
STUDENT_REF = db.collection("students")
WRONG_ANSWER_REF = db.collection("wrong_answers")
RIGHT_ANSWER_REF = db.collection("right_answers")
REGISTERED__REF = db.collection("contest_registeration")