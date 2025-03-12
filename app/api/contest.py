from fastapi import APIRouter, HTTPException
from app.schemas.contest import ContestSchema, ContestUpdateSchema
from app.services.contest_service import ContestService

router = APIRouter()

@router.get("/")
def get_all_contests():
    return {"contests": ContestService.get_all_contests()}

@router.get("/{contest_id}")
def get_contest_by_id(contest_id: str):
    contest = ContestService.get_contest_by_id(contest_id)
    if not contest:
        raise HTTPException(status_code=404, detail="Contest not found")
    return {"contest": contest}

@router.post("/add")
def add_contest(contest: ContestSchema):
    contest_id = ContestService.add_contest(contest.model_dump())
    return {"message": "success", "id": contest_id}

@router.put("/reschedule/{contest_id}")
def reschedule_contest(contest_id: str, contest: ContestUpdateSchema):
    ContestService.update_contest(contest_id, contest.model_dump(exclude_none=True))
    return {"message": "success"}

@router.delete("/delete/{contest_id}")
def delete_contest(contest_id: str):
    ContestService.delete_contest(contest_id)
    return {"message": "success"}

@router.get("/submissions")
def get_all_submissions():
    return {"submissions": ContestService.get_all_submissions()}

@router.get("/submissionswithstudent")
def get_submissions_with_student_info():
    return {"result": ContestService.get_submissions_with_student_info()}

@router.get("/grades")
def get_grades_and_schools():
    return ContestService.get_grades_and_schools()

