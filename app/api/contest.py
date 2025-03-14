from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from app.schemas.contest import ContestSchema, ContestUpdateSchema
from app.services.contest_service import ContestService

router = APIRouter()

@router.get("/")
async def get_all_contests():
    try:
        contests = ContestService.get_all_contests()
        return JSONResponse({"contests":contests })
    except Exception as e:
        return JSONResponse({"message":e},status_code=200)

@router.get("/{contest_id}")
async def get_contest_by_id(request:Request):
    data = await request.json()
    contest_id = data["contest_id"] 
    try:
        contest = ContestService.get_contest_by_id(contest_id)
        if not contest:
            return JSONResponse({"message":"contest not found"},status_code=404, detail="Contest not found")
        return JSONResponse({"contest": contest},status_code=200)
    except Exception as e:
        return JSONResponse({"message":e},status_code=500)

@router.post("/add")
async def add_contest(request:Request):
    data = await request.json()
    contest = data["contest"]
    try:
        contest_id = ContestService.add_contest(contest)
        return JSONResponse({"message": "success", "id": contest_id},status_code=200)
    except Exception as e:
        return JSONResponse({"message":e},status_code=500)

@router.put("/reschedule/{contest_id}")
async def reschedule_contest(request:Request):
    data = await request.json()
    contest_id, contest = data["contest_id"],data["contest"]
    try:

        ContestService.update_contest(contest_id, contest.model_dump(exclude_none=True))
        return JSONResponse({"message": "success"},status_code=200)
    except Exception as e:
        return JSONResponse({"message":e},status_code=500)

@router.delete("/delete/{contest_id}")
async def delete_contest(contest_id:str):
    try:
        ContestService.delete_contest(contest_id)
        return JSONResponse({"message": "success"},status_code=200)
    except Exception as e:
        return JSONResponse({"message":e},status_code=500)



