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
from app.api.statistics import router as statistics_router # Import statistics router
from app.api.leaderboard import router as leaderboard_router # Import leaderboard router    

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contest_router, prefix="/api/contest", tags=["contest"])
app.include_router(submission_router, prefix="/api/submission", tags=["submission"])
app.include_router(question_router, prefix="/api/question", tags=["question"])
app.include_router(student_router, prefix="/api/student", tags=["student"])
app.include_router(image_router, prefix="/api/image", tags=["image"])
app.include_router(admin_router, prefix="/api/admin", tags=["admin"])
app.include_router(feedback_router, prefix="/api/feedback", tags=["feedback"])
app.include_router(statistics_router, prefix="/api/statistics", tags=["statistics"]) # Include statistics router
app.include_router(leaderboard_router, prefix="/api/leaderboard", tags=["leaderboard"])