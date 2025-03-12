from pydantic import BaseModel
from typing import List, Optional

class QuestionSchema(BaseModel):
    question_text: str
    multiple_choice: List[str]
    answer: str
    explanation: str
    grade: str
    chapter: int

class QuestionUpdateSchema(BaseModel):
    question_text: Optional[str] = None
    multiple_choice: Optional[List[str]] = None
    answer: Optional[str] = None
    explanation: Optional[str] = None
    grade: Optional[str] = None
    chapter: Optional[int] = None
