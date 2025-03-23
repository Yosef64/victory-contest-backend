from fastapi import APIRouter, Request
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
async def update_question(request:Request):
    data = await request.json()
    question = data["question"]
    print(question)
    try:
        QuestionService.update_question(question)
        return JSONResponse({"message": "success"},status_code=200)
    except Exception as e:
        raise JSONResponse({"message":e},status_code=500, detail=str(e))

@router.delete("/deletequestion/{question_id}")
async def delete_question(request:Request,question_id:str):
    try:
        QuestionService.delete_question(question_id)
        return JSONResponse({"message": "success"},status_code=200)
    except Exception as e:
        raise JSONResponse({"message":e},status_code=500, detail=str(e))

@router.get("/missed-questions/{student}")
async def get_missed_questions(student: str):
    try:
        missed_questions = QuestionService.get_missed_questions(student)
        print(missed_questions)
        return JSONResponse({"missed_questions": missed_questions}, status_code=200)
    except Exception as e:
        return JSONResponse({"message":e},status_code=500)

@router.get("/weekly_missed_questions/{student_id}")
async def get_weekly_missed_questions(student_id: str):
    try:
        missed_questions = QuestionService.get_weekly_missed_questions(student_id)
        return JSONResponse({"missed_questions": missed_questions}, status_code=200)
    except Exception as e:
        return JSONResponse({"message":e},status_code=500)

@router.get("/monthly_missed_questions/{student_id}")
async def get_monthly_missed_questions(student_id: str):
    try:
        missed_questions = QuestionService.get_monthly_missed_questions(student_id)
        return JSONResponse({"missed_questions": missed_questions}, status_code=200)
    except Exception as e:
        return JSONResponse({"message":e},status_code=500)

@router.get("/missed_questions/{contest_id}/{student_id}")
async def get_missed_questions_by_contest(request: Request, contest_id: str, student_id: str):
    try:
        missed_questions = QuestionService.get_missed_questions_by_contest(contest_id, student_id)
        return JSONResponse({"missed_questions": missed_questions}, status_code=200)
    except Exception as e:
        return JSONResponse({"message": str(e)}, status_code=500)