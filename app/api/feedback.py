# app/api/feedback.py

from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse
from app.repositories.feedback_repo import FeedbackRepository
from app.services.feedback_service import FeedbackService
from app.schemas.feedback_schemas import FeedbackQuestionCreate, FeedbackQuestionUpdate, PollOptionCreate, PollOptionUpdate, FeedbackSubmission # Import necessary schemas
from typing import Optional

router = APIRouter()

# Feedback Questions Management (Admin)
@router.get("/questions")
async def get_all_questions():
    """Get all feedback questions for admin management"""
    try:
        questions = FeedbackRepository.get_all_questions()
        return JSONResponse({"questions": questions}, status_code=200)
    except Exception as e:
        return JSONResponse({"message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get("/questions/active")
async def get_active_questions():
    """Get only active questions for student feedback form"""
    try:
        questions = FeedbackRepository.get_active_questions()
        return JSONResponse({"questions": questions}, status_code=200)
    except Exception as e:
        return JSONResponse({"message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.post("/questions")
async def create_question(question_data: FeedbackQuestionCreate): # Use Pydantic model for request body
    """Create new feedback question"""
    try:
        new_question = FeedbackService.add_question(question_data.dict())
        return JSONResponse({"message": "Question created successfully", "question": new_question}, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        # It's good practice to log the full exception traceback here for debugging
        print(f"Error creating question: {e}", exc_info=True)
        return JSONResponse({"message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.put("/questions/{question_id}")
async def update_question(question_id: str, update_data: FeedbackQuestionUpdate): # Use Pydantic model for update
    """Update an existing feedback question"""
    try:
        success = FeedbackService.modify_question(question_id, update_data.dict(exclude_unset=True))
        if success:
            updated_question = FeedbackRepository.get_question_by_id(question_id)
            if updated_question:
                return JSONResponse({"message": "Question updated successfully", "question": updated_question}, status_code=200)
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found after update")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update question")
    except HTTPException as he:
        return JSONResponse({"message": he.detail}, status_code=he.status_code)
    except Exception as e:
        print(f"Error updating question {question_id}: {e}", exc_info=True)
        return JSONResponse({"message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.delete("/questions/{question_id}")
async def delete_question(question_id: str):
    """Delete a feedback question"""
    try:
        success = FeedbackService.remove_question(question_id)
        if success:
            return JSONResponse({"message": "Question deleted successfully"}, status_code=200)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to delete question")
    except Exception as e:
        print(f"Error deleting question {question_id}: {e}", exc_info=True)
        return JSONResponse({"message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.put("/questions/{question_id}/status")
async def toggle_question_status(question_id: str, request: Request):
    """Toggle the active status of a feedback question"""
    try:
        data = await request.json()
        is_active = data.get("isActive")
        if is_active is None or not isinstance(is_active, bool):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid 'isActive' status provided")

        success = FeedbackService.toggle_question_status(question_id, is_active)
        if success:
            updated_question = FeedbackRepository.get_question_by_id(question_id)
            if updated_question:
                return JSONResponse({"message": "Question status updated successfully", "question": updated_question}, status_code=200)
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found after status update")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to toggle question status")
    except HTTPException as he:
        return JSONResponse({"message": he.detail}, status_code=he.status_code)
    except Exception as e:
        print(f"Error toggling question status for {question_id}: {e}", exc_info=True)
        return JSONResponse({"message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Poll Options Management (Admin)
@router.post("/poll-options")
async def create_poll_option(poll_option_data: PollOptionCreate):
    """Create a new poll option"""
    try:
        new_option = FeedbackService.add_poll_option(poll_option_data.dict())
        return JSONResponse({"message": "Poll option created successfully", "option": new_option}, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        print(f"Error creating poll option: {e}", exc_info=True)
        return JSONResponse({"message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get("/poll-options")
async def get_all_poll_options():
    """Get all poll options for admin management"""
    try:
        options = FeedbackRepository.get_poll_options()
        return JSONResponse({"poll_options": options}, status_code=200)
    except Exception as e:
        print(f"Error getting all poll options: {e}", exc_info=True)
        return JSONResponse({"message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.put("/poll-options/{option_id}")
async def update_poll_option(option_id: str, update_data: PollOptionUpdate):
    """Update an existing poll option"""
    try:
        success = FeedbackService.modify_poll_option(option_id, update_data.dict(exclude_unset=True))
        if success:
            # Re-fetch the updated option to return the latest state (optional, but good for consistency)
            updated_option = next((opt for opt in FeedbackRepository.get_poll_options() if opt['id'] == option_id), None)
            if updated_option:
                return JSONResponse({"message": "Poll option updated successfully", "option": updated_option}, status_code=200)
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Poll option not found after update")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update poll option")
    except HTTPException as he:
        return JSONResponse({"message": he.detail}, status_code=he.status_code)
    except Exception as e:
        print(f"Error updating poll option {option_id}: {e}", exc_info=True)
        return JSONResponse({"message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.delete("/poll-options/{option_id}")
async def delete_poll_option(option_id: str):
    """Delete a poll option"""
    try:
        success = FeedbackService.remove_poll_option(option_id)
        if success:
            return JSONResponse({"message": "Poll option deleted successfully"}, status_code=200)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to delete poll option")
    except Exception as e:
        print(f"Error deleting poll option {option_id}: {e}", exc_info=True)
        return JSONResponse({"message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Feedback Responses (Student Submission)
@router.post("/responses")
async def submit_feedback(feedback_data: FeedbackSubmission):
    """Submit student feedback"""
    try:
        response_id = FeedbackService.submit_feedback(feedback_data.dict())
        return JSONResponse({"message": "Feedback submitted successfully", "response_id": response_id}, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        print(f"Error submitting feedback: {e}", exc_info=True)
        return JSONResponse({"message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get("/responses")
async def get_all_responses():
    """Get all feedback responses for admin management"""
    try:
        responses = FeedbackRepository.get_feedback_responses()
        return JSONResponse({"responses": responses}, status_code=200)
    except Exception as e:
        print(f"Error getting all responses: {e}", exc_info=True)
        return JSONResponse({"message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.delete("/responses/{response_id}")
async def delete_feedback_response(response_id: str):
    """Delete a feedback response by ID"""
    try:
        FeedbackService.delete_feedback_response(response_id)
        return JSONResponse({"message": "Feedback response deleted successfully"}, status_code=200)
    except Exception as e:
        print(f"Error deleting feedback response {response_id}: {e}", exc_info=True)
        return JSONResponse({"message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Analytics
@router.get("/analytics")
async def get_feedback_analytics(request: Request):
    """Get feedback analytics data"""
    try:
        params = request.query_params
        time_range = params.get("range", "all")

        analytics = FeedbackService.get_analytics(time_range)
        return JSONResponse({"analytics": analytics}, status_code=200)
    except Exception as e:
        print(f"Error getting analytics: {e}", exc_info=True)
        return JSONResponse({"message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get("/high-scorers")
async def get_high_scorers():
    """Get list of high-scoring students with contact info"""
    try:
        high_scorers = FeedbackService.get_high_scorers()
        return JSONResponse({"high_scorers": high_scorers}, status_code=200)
    except Exception as e:
        print(f"Error getting high scorers: {e}", exc_info=True)
        return JSONResponse({"message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
