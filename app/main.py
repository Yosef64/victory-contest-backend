from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.contest import router as contest_router
from app.api.submission import router as submission_router
from app.api.question import router as question_router
from app.api.students import router as student_router
from app.api.image import router as image_router
from app.api.admin import router as admin_router
from app.api.feedback import router as feedback_router # NEW: Import the feedback router

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

#cors origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://7wwb0knl-5173.euw.devtunnels.ms",
        "https://victory-admin-page.vercel.app",
        "http://localhost:5173",
        "https://victory-contest.vercel.app"# Optional, depending on how it's opened
    ],
    allow_credentials=True,
    allow_methods=["*"],          
    allow_headers=["*"],          
)

#initial routes
app.include_router(student_router, prefix="/api/student", tags=["Students"])
app.include_router(submission_router, prefix="/api/submission", tags=["Submissions"])
app.include_router(contest_router, prefix="/api/contest", tags=["Contests"])
app.include_router(question_router, prefix="/api/question", tags=["Questions"])
app.include_router(image_router, prefix="/api/image", tags=["Images"])
app.include_router(admin_router,prefix="/api/admin", tags=["Admin"]) # Corrected missing closing quote and tag
app.include_router(feedback_router, prefix="/api/feedback", tags=["Feedback"]) # NEW: Include the feedback router
