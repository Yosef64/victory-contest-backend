from pydantic import BaseModel

class MenuItem(BaseModel):
    id: int
    title: str
    path: str