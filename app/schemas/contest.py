from pydantic import BaseModel
from typing import List, Optional

class ContestSchema(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: str
    end_time: str
    max_participants: Optional[int] = None
    prize: str
class ContestUpdateSchema(BaseModel):
    start_time: Optional[str] = None
    end_time: Optional[str] = None

class SubmissionSchema(BaseModel):
    student_id: str
    contest_id: str
    score: int
