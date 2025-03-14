from fastapi import APIRouter, HTTPException,Request
from fastapi.responses import JSONResponse
from app.services.student_service import (
    create_student, fetch_students, fetch_student_by_id, 
    modify_student, verify_student_paid, fetch_paid_students
)
from app.schemas.student import StudentCreate, StudentUpdate

router = APIRouter()

@router.post("/", response_model=dict)
async def add_student(request:Request):
    data = await request.json()
    student = data["student"]
    return create_student(student)

@router.get("/", response_model=dict)
def get_students():
    students = fetch_students()
    return JSONResponse({"message":students},status_code=200)

@router.get("/{student_id}", response_model=dict)
async def get_student_by_id(request:Request):
    try:
        data = await request.json()
        student_id = data["student_id"]
        student, status_code = fetch_student_by_id(student_id)
        if status_code == 404:
            raise HTTPException(status_code=404, detail=student["message"])
        elif status_code == 500:
            raise HTTPException(status_code=500, detail=student["error"])
        return JSONResponse({"student":student},status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.put("/{student_id}", response_model=dict)
async def update_student(request:Request):
    data = await request.json()
    student_id,student_data = data["student_id"],data["student_id"]
    modify_student(student_id, student_data)
    return JSONResponse({"message":"ok"},status_code=200)

@router.get("/{student_id}/paid", response_model=dict)
async def check_student_paid(request:Request):
    data = await request.json()
    status = verify_student_paid(data["student_id"])
    return JSONResponse({"message":status},status_code=200)

@router.get("/paid", response_model=dict)
async def get_paid_students(request:Request):
    response = fetch_paid_students()

    if not isinstance(response, tuple) or len(response) != 2:
        raise HTTPException(status_code=500, detail="Unexpected response format")

    response_data, status_code = response

    if status_code == 404:
        raise HTTPException(status_code=404, detail=response_data["message"])
    elif status_code == 500:
        raise HTTPException(status_code=500, detail=response_data["error"])

    return JSONResponse({"message":response_data},status_code=200)  # Successfully return students


