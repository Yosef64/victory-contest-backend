from fastapi import APIRouter, HTTPException, Depends
from app.schemas.question import QuestionSchema, QuestionUpdateSchema
from app.services.question_service import QuestionService

router = APIRouter()

@router.get("/questions")
def get_questions():
    return {"questions": QuestionService.get_questions()}

@router.post("/addquestion")
def add_question(question: QuestionSchema):
    try:
        question_id = QuestionService.add_question(question.dict())
        return {"message": "success", "id": question_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/updatequestion/{question_id}")
def update_question(question_id: str, question: QuestionUpdateSchema):
    try:
        QuestionService.update_question(question_id, question.dict(exclude_none=True))
        return {"message": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/deletequestion/{question_id}")
def delete_question(question_id: str):
    try:
        QuestionService.delete_question(question_id)
        return {"message": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
