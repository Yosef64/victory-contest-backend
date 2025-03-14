from fastapi import APIRouter, HTTPException, Depends, Request
from app.schemas.question import QuestionSchema, QuestionUpdateSchema
from fastapi.responses import JSONResponse
from app.services.question_service import QuestionService

router = APIRouter()

@router.get("/")
async def get_questions():
    questions = QuestionService.get_questions()
    return JSONResponse({"questions":questions },status_code=200)

@router.post("/addquestion")
async def add_question(request:Request):
    data = await request.json()
    question = data["question"]
    try:
        question_id = QuestionService.add_question(question)
        return JSONResponse({"message": "success", "id": question_id},status_code=200)
    except Exception as e:
        return JSONResponse({"message":e},status_code=500, detail=str(e))
@router.post("/addQuestions")
async def addQuestions(request:Request):
    data = await request.json()
    questions = data["questions"]
    try:
        QuestionService.add_questions(questions)
        return JSONResponse({"message":"success"},status_code=200)
    except Exception as e:
        return JSONResponse({"message":e},status_code=500)
@router.put("/updatequestion/{question_id}")
async def update_question(request):
    data = await request.json()
    question = data["question"]
    try:
        QuestionService.update_question(question.dict(exclude_none=True))
        return JSONResponse({"message": "success"},status_code=200)
    except Exception as e:
        raise JSONResponse({"message":e},status_code=500, detail=str(e))

@router.delete("/deletequestion/{question_id}")
async def delete_question(request):
    data = await request.json()
    question_id = data["question_id"]
    try:
        QuestionService.delete_question(question_id)
        return JSONResponse({"message": "success"},status_code=200)
    except Exception as e:
        raise JSONResponse({"message":e},status_code=500, detail=str(e))
