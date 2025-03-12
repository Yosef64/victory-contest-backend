from fastapi import APIRouter, HTTPException
from app.schemas.submission import SubmissionSchema
from app.services.submission_service import SubmissionService

router = APIRouter()

@router.get("/submissions")
def get_all_submissions():
    return {"submissions": SubmissionService.get_all_submissions()}

@router.get("/submissionswithstudent")
def get_submissions_with_student_info():
    return {"result": SubmissionService.get_submissions_with_student_info()}

@router.get("/grades")
def get_grades_and_schools():
    return SubmissionService.get_grades_and_schools()

@router.post("/submission", response_model=dict)
def submit_submission(submission: SubmissionService.SubmissionSchema):
    response, status_code = SubmissionService.create_submission(submission)

    if status_code == 500:
        raise HTTPException(status_code=500, detail=response["error"])

    return response