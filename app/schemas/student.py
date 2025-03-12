from pydantic import BaseModel
from typing import Optional

class StudentBase(BaseModel):
    telegram_id: str
    name: str
    age: int
    grade: str
    school: str
    paid: bool = False

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    grade: Optional[str] = None
    school: Optional[str] = None
    paid: Optional[bool] = None
