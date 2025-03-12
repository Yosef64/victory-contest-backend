from pydantic import BaseModel, HttpUrl
from typing import List

class StudentSchema(BaseModel):
    student_id: str
    img_url: str
    name: str

class SubmissionSchema(BaseModel):
    student: StudentSchema
    contest_id: str
    submission_time: str  # ISO format: YYYY-MM-DDTHH:MM:SS
    score: int
    wrong_answers: List[str]
