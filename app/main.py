from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.contest import router as contest_router
from app.api.submission import router as submission_router
from app.api.question import router as question_router
from app.api.students import router as student_router 
from app.api.image import router as image_router
from app.api.admin import router as admin_router
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

#cors origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://localhost:5174","https://victory-contest.vercel.app","https://victory-admin-page.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],  
    )

#initial routes
app.include_router(student_router, prefix="/api/student", tags=["Students"])
app.include_router(submission_router, prefix="/api/submission", tags=["Submissions"])
app.include_router(contest_router, prefix="/api/contest", tags=["Contests"])
app.include_router(question_router, prefix="/api/question", tags=["Questions"])
app.include_router(image_router, prefix="/api/image", tags=["Images"])
app.include_router(admin_router,prefix="/api/admin",tags=["Admin"]
)
@app.get("/")
async def root(request:Request):
    return JSONResponse({"message": "Welcome to the API!"},status_code=200)
