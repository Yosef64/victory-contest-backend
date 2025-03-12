from app.db.firebase import db
from app.schemas.student import StudentCreate, StudentUpdate

STUDENT_REF = db.collection("students")

def add_student(student: StudentCreate):
    student_id = student.telegram_id
    STUDENT_REF.document(student_id).set(student.model_dump())
    return {"message": "Student added successfully"}

def get_students():
    return [doc.id for doc in STUDENT_REF.stream()]

def get_student_by_id(student_id: str):
    try:
        student_doc = STUDENT_REF.document(student_id).get()
        if not student_doc.exists:
            return None  # Return None if student does not exist
        return student_doc.to_dict()  # Return student data
    except Exception as e:
        return {"error": str(e)}


def update_student(student_id: str, student_data: StudentUpdate):
    STUDENT_REF.document(student_id).update(student_data.model_dump(exclude_unset=True))
    return {"message": "Student updated successfully"}

def check_student_paid(student_id: str):
    student = STUDENT_REF.document(student_id).get()
    if not student.exists:
        return None
    return student.to_dict().get("paid", False)

def get_paid_students():
    try:
        students = []
        for doc in STUDENT_REF.stream():
            student = doc.to_dict()
            if student and student.get("paid") is True:  # Safe lookup for "paid"
                students.append(student)

        print(f"✅ Retrieved {len(students)} paid students.")  # Debugging
        return students  # Returns an empty list if no students found

    except Exception as e:
        print(f"🔥 Database error: {e}")  # Log the exact database error
        return None  # Ensure failure returns None





