from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from app.schemas.submission import SubmissionSchema
from app.services.submission_service import SubmissionService

router = APIRouter()

@router.get("/")
async def get_all_submissions():
    try:
        submissions = SubmissionService.get_all_submissions()
        return JSONResponse({"submissions": submissions},status_code=200)
    except Exception as e:
        return JSONResponse({"message":e},status_code=500)
@router.get("/contest_id/{contest_id}")
async def get_all_submission_by_contest(request:Request,contest_id:str):
    try:
        submission = SubmissionService.get_submissions_by_contest(contest_id)
        return JSONResponse({"submissions":submission},status_code=200)
    except Exception as e:
        return JSONResponse({"message":e},status_code=500)
@router.get("/submissionswithstudent")
async def get_submissions_with_student_info():
    try:
        submissions_with_student_info = SubmissionService.get_submissions_with_student_info()
        return JSONResponse({"result": submissions_with_student_info},status_code=200)
    except Exception as e:
        return JSONResponse({"message":e},status_code=500)

@router.get("/grades")
async def get_grades_and_schools():
    try:

        getGradesAndSchools = SubmissionService.get_grades_and_schools()
        return JSONResponse({"messages":get_grades_and_schools},status_code=200)
    except Exception as e:
        return JSONResponse({"message":e},status_code=500)

@router.post("/submission", response_model=dict)
async def submit_submission(request:Request):
    data = await request.json()
    submission = data["submission"]
    try:
        response, status_code = SubmissionService.create_submission(submission)
        return JSONResponse({"message":response},status_code=200)
    except Exception as e:
        return JSONResponse({"message":e},status_code=500)