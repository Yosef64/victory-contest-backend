from typing import List, Optional
from pydantic import BaseModel
from fastapi import APIRouter, File, Form, Request, UploadFile
from fastapi.responses import JSONResponse
from app.services.question_service import QuestionService

router = APIRouter()
# Pydantic model for the question
class QuestionCreate(BaseModel):
    question_text: str
    multiple_choice: List[str] = []
    answer: str
    explanation: str
    grade: str
    chapter: str
    subject: str
    question_image: Optional[bytes] = None
    question_image_filename: Optional[str] = None
    explanation_image: Optional[bytes] = None
    explanation_image_filename: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "question_text": "What is 2+2?",
                "multiple_choice": ["1", "2", "3", "4"],
                "answer": "4",
                "explanation": "2+2 equals 4",
                "grade": "5",
                "chapter": "Arithmetic",
                "subject": "Math"
            }
        }
@router.get("/")
async def get_questions():
    questions = QuestionService.get_questions()
    return JSONResponse({"questions":questions },status_code=200)

@router.post("/addquestion")
async def add_question(question_text: str = Form(...),
    multiple_choice: List[str] = Form(default=[]),
    answer: str = Form(...),
    explanation: str = Form(...),
    grade: str = Form(...),
    chapter: str = Form(...),
    subject: str = Form(...),
    question_image: Optional[UploadFile] = File(None),
    explanation_image: Optional[UploadFile] = File(None)):

    try:
        print("Received multiple_choice:", multiple_choice)

        question_data = {
            "question_text": question_text,
            "multiple_choice": multiple_choice or [],
            "answer": answer,
            "explanation": explanation,
            "grade": grade,
            "chapter": chapter,
            "subject": subject,
            "question_image": question_image,
            "explanation_image": explanation_image,
        }
        # print(question_data)
        QuestionService.add_question(question_data)
        return JSONResponse({"message": "Question added successfully"}, status_code=200)
        
    except Exception as e:
        print(str(e))
        return JSONResponse({"message": str(e)}, status_code=500)
@router.post("/addQuestions")
async def addQuestions(request:Request):
    data = await request.json()
    questions = data["questions"]
    try:
        QuestionService.add_questions(questions)
        return JSONResponse({"message":"success"},status_code=200)
    except Exception as e:
        return JSONResponse({"message": str(e)}, status_code=500)
@router.put("/updatequestion/{question_id}")
async def update_question(request:Request):
    data = await request.json()
    question = data["question"]
    print(question)
    try:
        QuestionService.update_question(question)
        return JSONResponse({"message": "success"},status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse({"message": str(e)}, status_code=500)

@router.delete("/deletequestion/{question_id}")
async def delete_question(request:Request,question_id:str):
    try:
        QuestionService.delete_question(question_id)
        return JSONResponse({"message": "success"},status_code=200)
    except Exception as e:
        return JSONResponse({"message": str(e)}, status_code=500)

@router.get("/missed-questions/{student}")
async def get_missed_questions(student: str):
    try:
        missed_questions = QuestionService.get_missed_questions(student)
        print(missed_questions)
        return JSONResponse({"missed_questions": missed_questions}, status_code=200)
    except Exception as e:
        return JSONResponse({"message": str(e)}, status_code=500)

@router.get("/weekly_missed_questions/{student_id}")
async def get_weekly_missed_questions(student_id: str):
    try:
        missed_questions = QuestionService.get_weekly_missed_questions(student_id)
        return JSONResponse({"missed_questions": missed_questions}, status_code=200)
    except Exception as e:
        return JSONResponse({"message": str(e)}, status_code=500)

@router.get("/monthly_missed_questions/{student_id}")
async def get_monthly_missed_questions(student_id: str):
    try:
        missed_questions = QuestionService.get_monthly_missed_questions(student_id)
        return JSONResponse({"missed_questions": missed_questions}, status_code=200)
    except Exception as e:
        return JSONResponse({"message": str(e)}, status_code=500)

@router.get("/missed_questions/{contest_id}/{student_id}")
async def get_missed_questions_by_contest(request: Request, contest_id: str, student_id: str):
    try:
        missed_questions = QuestionService.get_missed_questions_by_contest(contest_id, student_id)
        return JSONResponse({"missed_questions": missed_questions}, status_code=200)
    except Exception as e:
        return JSONResponse({"message": str(e)}, status_code=500)