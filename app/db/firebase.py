import os
import base64
import json
import firebase_admin
from firebase_admin import credentials, firestore

base64_key = os.getenv("FIREBASE_CREDENTIALS") 

if base64_key:
    firebase_key_json = json.loads(base64.b64decode(base64_key).decode('utf-8'))
    cred = credentials.Certificate(firebase_key_json)
    
else:
    cred = credentials.Certificate("app/db/key.json")

firebase_admin.initialize_app(cred)

db = firestore.client()
QUESTION_REF = db.collection("questions")
CONTEST_REF = db.collection("contests")
SUBMISSION_REF = db.collection("submissions")
STUDENT_REF = db.collection("students")
WRONG_ANSWER_REF = db.collection("wrong_answers")
RIGHT_ANSWER_REF = db.collection("right_answers")
REGISTERED__REF = db.collection("contest_registeration")