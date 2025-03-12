from app.repositories.student_repo import (
    add_student, get_students, get_student_by_id, update_student,
    check_student_paid, get_paid_students
)
from app.schemas.student import StudentCreate, StudentUpdate

def create_student(student: StudentCreate):
    return add_student(student)

def fetch_students():
    return {"students": get_students()}

def fetch_student_by_id(student_id: str):
    try:
        student = get_student_by_id(student_id)
        if student is None:
            return {"message": "Student not found"}, 404
        elif isinstance(student, dict) and "error" in student:
            return student, 500  # Error occurred in repo layer
        return {"student": student}, 200
    except Exception as e:
        return {"error": str(e)}, 500

def modify_student(student_id: str, student_data: StudentUpdate):
    return update_student(student_id, student_data)

def verify_student_paid(student_id: str):
    status = check_student_paid(student_id)
    if status is None:
        return {"message": None}
    return {"message": status}

def fetch_paid_students():
    try:
        students = get_paid_students()

        if students is None:  # Check for database error
            print("🚨 Error: Failed to fetch students from Firestore.")  # Debugging
            return {"error": "Failed to fetch students from database"}, 500
        
        if not students:  # If list is empty, return 404
            print("⚠️ No paid students found.")  # Debugging
            return {"message": "No paid students found"}, 404
        
        return {"paid_students": students}, 200

    except Exception as e:
        print(f"🔥 Internal Server Error: {e}")  # Debugging in console
        return {"error": f"Internal server error: {str(e)}"}, 500


