from fastapi import APIRouter, HTTPException,Request
from fastapi.responses import JSONResponse
from app.services.student_service import StudentService
from app.schemas.student import StudentCreate, StudentUpdate
from app.services.notification_service import NotificationService
from app.repositories.student_repo import StudentRepository
from app.repositories.badge_repo import BadgeRepository
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
@router.post("/register")
async def register_student(student: StudentCreate, request: Request):
    try:
        # Save student to database
        student_data = student.dict()
        StudentService.add_student(student_data)
        
        # Create notification for admin
        notification_msg = f"New student registered: {student_data['name']}"
        NotificationService.create_personal_notification(
            student_id="admin",  # Or get admin ID from your system
            message=notification_msg,
            notification_type="registration",
            title="New Student Registration",
        )
        
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

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

@router.get("/rank/{contest_id}", response_model=dict)
async def get_student_rankings_by_contest(contest_id: str):
    try:
        rankings = StudentService.get_student_rankings_by_contest(contest_id)
        return JSONResponse({"rankings": rankings}, status_code=200)
    except Exception as e:
        return JSONResponse({"message": str(e)}, status_code=500)

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
# Add new endpoint for grades and schools
@router.get("/grades-and-schools")
async def get_grades_and_schools():
    try:
        data = StudentRepository.get_grades_and_schools()
        return JSONResponse(data, status_code=200)
    except Exception as e:
        return JSONResponse({"message": str(e)}, status_code=500)

@router.get("/profile/{student_id}", response_model=dict)
def get_user_profile(request:Request,student_id:str):
    try:

        user = StudentService.get_user_profile(student_id)
        return JSONResponse({"user": user}, status_code=200)
    except Exception as e:
        return JSONResponse({"message": str(e)}, status_code=500)

@router.get("/statistics/{student_id}")
def get_student_statistics(student_id: str):
    try:
        stats = StudentRepository.get_user_statistics(student_id)
        return JSONResponse({"message":stats},status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse({"message": str(e)}, status_code=500)
@router.get("/student/{student_id}/badge")
def get_student_submissions(student_id: str):
    try:
        submissions = BadgeRepository.get_user_badges(student_id)
        return JSONResponse({"submissions": submissions}, status_code=200)
    except Exception as e:
        return JSONResponse({"message": str(e)}, status_code=500)
@router.get("/editorial/{student_id}")
async def get_student_editorial(request: Request, student_id: str):

    constest_id = request.query_params.get("contest_id")
    if not constest_id:
        return JSONResponse({"message": "contest_id is required"}, status_code=400)
    try:
        editorial = StudentService.get_student_editorial(student_id,constest_id)
        return JSONResponse({"editorial": editorial}, status_code=200)
    except Exception as e:
        return JSONResponse({"message": str(e)}, status_code=500)
