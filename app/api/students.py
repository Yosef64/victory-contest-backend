from fastapi import APIRouter, HTTPException,Request
from fastapi.responses import JSONResponse
from app.services.student_service import StudentService
from app.schemas.student import StudentCreate, StudentUpdate

router = APIRouter()

@router.post("/", response_model=dict)
async def add_student(request:Request):
    data = await request.json()
  
    try:
        student = data["student"]
        StudentService.add_student(student)
        return JSONResponse({"message":"success"},status_code=200)
    except Exception as e:
        return JSONResponse({"message":e},status_code=200)

@router.get("/", response_model=dict)
def get_students():
    students = StudentService.get_students()
    return JSONResponse({"message":students},status_code=200)


@router.get("/paid", response_model=dict)
async def get_paid_students(request:Request):
    response = StudentService.get_paid_students()

    if not isinstance(response, tuple) or len(response) != 2:
        raise HTTPException(status_code=500, detail="Unexpected response format")

    response_data, status_code = response

    if status_code == 404:
        raise HTTPException(status_code=404, detail=response_data["message"])
    elif status_code == 500:
        raise HTTPException(status_code=500, detail=response_data["error"])

    return JSONResponse({"message":response_data},status_code=200)  # Successfully return students

@router.get("/quickstat/{student_id}")
async def get_quick_stat(request:Request,student_id:str):
    try:
        stat = StudentService.get_quick_stat(student_id)
        return JSONResponse({"stat":stat},status_code=200)
    except Exception as e:
        return JSONResponse({"message":e},status_code=500,)

@router.get("/rank", response_model=dict)
async def get_student_rankings():
    rankings = StudentService.get_student_rankings()
    return JSONResponse({"rankings": rankings}, status_code=200)
    

@router.get("/{student_id}", response_model=dict)
async def get_student_by_id(request:Request,student_id:str):
    try:
        student = StudentService.get_student_by_id(student_id)
        return JSONResponse({"student":student},status_code=200)
    except Exception as e:
        return JSONResponse({"message":e},status_code=500,)

@router.put("/{student_id}", response_model=dict)
async def update_student(request:Request):
    data = await request.json()
    student = data["student"]
    StudentService.update_student(student)
    return JSONResponse({"message":"ok"},status_code=200)

@router.get("/{student_id}/paid", response_model=dict)
async def check_student_paid(request:Request):
    data = await request.json()
    status = StudentService.verify_student_paid(data["telegram_id"])
    return JSONResponse({"message":status},status_code=200)