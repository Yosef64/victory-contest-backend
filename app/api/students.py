from fastapi import APIRouter, HTTPException
from app.services.student_service import (
    create_student, fetch_students, fetch_student_by_id, 
    modify_student, verify_student_paid, fetch_paid_students
)
from app.schemas.student import StudentCreate, StudentUpdate

router = APIRouter()

@router.post("/", response_model=dict)
def add_student(student: StudentCreate):
    return create_student(student)

@router.get("/", response_model=dict)
def get_students():
    return fetch_students()

@router.get("/{student_id}", response_model=dict)
def get_student_by_id(student_id: str):
    try:
        student, status_code = fetch_student_by_id(student_id)
        if status_code == 404:
            raise HTTPException(status_code=404, detail=student["message"])
        elif status_code == 500:
            raise HTTPException(status_code=500, detail=student["error"])
        return student
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.put("/{student_id}", response_model=dict)
def update_student(student_id: str, student_data: StudentUpdate):
    return modify_student(student_id, student_data)

@router.get("/{student_id}/paid", response_model=dict)
def check_student_paid(student_id: str):
    return verify_student_paid(student_id)

@router.get("/paid", response_model=dict)
def get_paid_students():
    response = fetch_paid_students()

    # Ensure response is a tuple before unpacking
    if not isinstance(response, tuple) or len(response) != 2:
        print(f"🚨 Unexpected response format: {response}")  # Debugging
        raise HTTPException(status_code=500, detail="Unexpected response format")

    response_data, status_code = response

    if status_code == 404:
        raise HTTPException(status_code=404, detail=response_data["message"])
    elif status_code == 500:
        raise HTTPException(status_code=500, detail=response_data["error"])

    return response_data  # Successfully return students


