from fastapi import FastAPI
from app.api.contest import router as contest_router
from app.api.submission import router as submission_router
from app.api.question import router as question_router
from app.api.students import router as student_router  # Fixed import

app = FastAPI(title="Contest-Based System API", version="1.0")

# Register API routers
app.include_router(student_router, prefix="/api/student", tags=["Students"])
app.include_router(submission_router, prefix="/api/submission", tags=["Submissions"])
app.include_router(contest_router, prefix="/api/contest", tags=["Contests"])
app.include_router(question_router, prefix="/api/question", tags=["Questions"])

@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to FastAPI with Firebase"}
