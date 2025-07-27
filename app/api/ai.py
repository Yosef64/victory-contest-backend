
import json
from typing import List
import google.generativeai as genai
from fastapi import APIRouter, HTTPException, Request, UploadFile, Form, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List
import os
router = APIRouter()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')
router = APIRouter()

class PracticeSettings(BaseModel):
    subject: str = Field(..., example="Mathematics")
    grade: str = Field(..., example="10")
    difficulty: str = Field(..., example="medium", pattern="^(easy|medium|hard)$")

class AIQuestion(BaseModel):
    question_text: str
    question_image: str | None = None
    multiple_choice: List[str]
    answer: int 
    explanation: str
    subject: str
    grade: str
    chapter: str
    
@router.post("/generate-session", response_model=List[AIQuestion])
async def generate_session(settings: PracticeSettings):
    """Generates a specific number of questions using the Gemini API."""

    prompt = f"""
    Generate 25 practice questions for a student.
    The topic is {settings.subject} for grade {settings.grade} at a {settings.difficulty} difficulty level.

    For each question, provide the following in a clear, structured format:
    - The question text.
    - Four multiple-choice options.
    - The index of the correct answer (0, 1, 2, or 3).
    - A brief explanation for the correct answer.

    IMPORTANT: Format the entire output as a JSON array where each element is a question object.
    Each object must have these exact keys: "question_text", "multiple_choice", "answer", "explanation", "subject", "grade", "chapter".
    """
    try:
        response = model.generate_content(prompt)
        raw_text = response.text
        start_index = raw_text.find('[')
        end_index = raw_text.rfind(']')

        if start_index == -1 or end_index == -1:
            raise ValueError("Could not find a JSON array in the response.")

        json_str = raw_text[start_index : end_index + 1]
        questions_data = json.loads(json_str)
        return JSONResponse({"message":questions_data},status_code=200)

    except Exception as e:
        print(f"Error generating questions: {e}")
        return JSONResponse(
            {"error": "Failed to generate questions", "details": str(e)},
            status_code=500
        )
