# app/services/feedback_service.py

from app.repositories.feedback_repo import FeedbackRepository
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import re
from app.schemas.feedback_schemas import FeedbackQuestionCreate, FeedbackQuestionUpdate, PollOptionCreate, PollOptionUpdate, FeedbackSubmission, ContactInfo # Import necessary schemas

class FeedbackService:

    @staticmethod
    def submit_feedback(feedback_data: Dict) -> str:
        """Process and submit student feedback"""

        # Validate data using Pydantic schema
        validated_data = FeedbackSubmission(**feedback_data).dict(exclude_unset=True)

        # Process contact info if provided (Pydantic already validates, this is for additional checks if needed)
        if validated_data.get("contact_info"):
            contact_info = validated_data["contact_info"]

            # The phone number and score validation are now primarily handled by Pydantic's ContactInfo schema.
            # Keeping these checks here for additional business logic, but they might be redundant.
            if not FeedbackService._validate_phone_number(contact_info.get("phone_number", "")):
                # This specific check might still be useful if _validate_phone_number has custom logic
                # beyond what Pydantic's regex handles, or if you want a specific error message.
                raise Exception("Invalid phone number format")

            score = contact_info.get("score", 0)
            if not isinstance(score, (int, float)) or score < 0 or score > 600:
                # This check is also covered by Pydantic's ContactInfo score validator.
                raise Exception("Score must be between 0 and 600")

        # Clean and process comment
        if validated_data.get("comment"):
            validated_data["comment"] = FeedbackService._clean_comment(validated_data["comment"])

        # Save to database
        response_id = FeedbackRepository.create_feedback_response(validated_data)

        # Check if notification is needed for high scorer
        poll_options = FeedbackRepository.get_poll_options()
        selected_poll_option = next((opt for opt in poll_options if opt['id'] == validated_data.get('poll_response')), None)

        if selected_poll_option and selected_poll_option.get('requiresContact') and validated_data.get('contact_info'):
            FeedbackService._notify_admin_high_scorer(validated_data)

        return response_id

    @staticmethod
    def _validate_feedback_data(data: Dict):
        """Internal method to validate feedback data structure and content."""
        # This validation is now handled by Pydantic schemas in the API layer,
        # but maintaining the method for potential additional business logic validation.
        pass

    @staticmethod
    def _validate_phone_number(phone_number: str) -> bool:
        """Validate Ethiopian phone number format."""
        patterns = [
            r'^\+2519\d{8}$',  # +2519XXXXXXXX
            r'^09\d{8}$',      # 09XXXXXXXX
            r'^9\d{8}$'        # 9XXXXXXXX
        ]
        # Corrected line: Iterate through patterns to apply re.fullmatch
        return any(re.fullmatch(pattern, phone_number) for pattern in patterns)

    @staticmethod
    def _clean_comment(comment: str) -> str:
        """Clean and normalize comment text."""
        cleaned_comment = comment.strip()
        # You can add more cleaning logic here, e.g., profanity filtering, emoji removal
        return cleaned_comment

    @staticmethod
    def get_analytics(time_range: str = "all") -> Dict:
        """Get feedback analytics based on time range."""
        # For simplicity, time_range filtering is not implemented in repo yet.
        # It would involve passing a date range to get_feedback_responses.
        question_stats = FeedbackRepository.get_question_statistics()
        poll_stats = FeedbackRepository.get_poll_statistics()
        contact_list = FeedbackRepository.get_contact_list_from_responses()

        responses = FeedbackRepository.get_feedback_responses(limit=1000) # Fetch all for calculation
        total_responses = len(responses)
        total_comments = sum(1 for r in responses if r.get("comment"))
        total_comment_length = sum(len(r.get("comment", "")) for r in responses)

        average_comment_length = total_comment_length / total_comments if total_comments > 0 else 0

        # Simple sentiment analysis (placeholder)
        all_comments = [r.get("comment", "") for r in responses if r.get("comment")]
        sentiment_score = FeedbackService._calculate_sentiment(all_comments)

        return {
            "totalResponses": total_responses,
            "questionStats": question_stats,
            "pollStats": poll_stats,
            "contactList": contact_list,
            "commentSummary": {
                "totalComments": total_comments,
                "averageLength": round(average_comment_length, 1),
                "sentimentScore": round(sentiment_score, 1)
            }
        }

    @staticmethod
    def get_high_scorers() -> List[Dict]:
        """Get a list of high-scoring students with contact info."""
        return FeedbackRepository.get_contact_list_from_responses() # Directly use repo method

    @staticmethod
    def delete_feedback_response(response_id: str):
        """Delete a feedback response."""
        FeedbackRepository.delete_feedback_response(response_id)

    @staticmethod
    def _calculate_sentiment(comments: List[str]) -> float:
        """
        A very basic sentiment analysis placeholder.
        Returns a score from 1 (negative) to 5 (positive), with 3 being neutral.
        """
        positive_words = {"good", "great", "excellent", "happy", "positive", "helpful", "amazing", "love"}
        negative_words = {"bad", "poor", "terrible", "unhappy", "negative", "awful", "hate"}

        total_score = 0
        total_words = 0

        for comment in comments:
            words = comment.lower().split()
            comment_score = 0

            for word in words:
                if word in positive_words:
                    comment_score += 1
                elif word in negative_words:
                    comment_score -= 1

            total_score += comment_score
            total_words += len(words)

        if total_words == 0:
            return 3.0  # Neutral

        normalized_score = 3.0 + (total_score / total_words) * 2
        return max(1.0, min(5.0, normalized_score))

    @staticmethod
    def _notify_admin_high_scorer(feedback_data: Dict):
        """Send notification to admin about high scorer"""
        contact_info = feedback_data.get("contact_info", {})
        student_name = feedback_data.get("student_name", "Anonymous")
        score = contact_info.get("score", 0)

        print(f"HIGH SCORER ALERT: {student_name} scored {score}")

    @staticmethod
    def add_question(question_data: Dict) -> Dict:
        """Add a new feedback question."""
        validated_data = FeedbackQuestionCreate(**question_data).dict(exclude_unset=True)
        return FeedbackRepository.create_question(validated_data)

    @staticmethod
    def modify_question(question_id: str, update_data: Dict) -> bool:
        """Update an existing feedback question."""
        validated_data = FeedbackQuestionUpdate(**update_data).dict(exclude_unset=True)
        return FeedbackRepository.update_question(question_id, validated_data)

    @staticmethod
    def remove_question(question_id: str) -> bool:
        """Remove a feedback question."""
        return FeedbackRepository.delete_question(question_id)

    @staticmethod
    def toggle_question_status(question_id: str, is_active: bool) -> bool:
        """Toggle the active status of a feedback question."""
        # Note: Frontend sends 'isActive', backend expects 'is_active' for Firestore.
        # The update_question in repo handles this key conversion.
        return FeedbackRepository.update_question(question_id, {"isActive": is_active})

    @staticmethod
    def add_poll_option(poll_option_data: Dict) -> Dict:
        """Add a new poll option."""
        validated_data = PollOptionCreate(**poll_option_data).dict(exclude_unset=True)
        return FeedbackRepository.create_poll_option(validated_data)

    @staticmethod
    def modify_poll_option(option_id: str, update_data: Dict) -> bool:
        """Update an existing poll option."""
        validated_data = PollOptionUpdate(**update_data).dict(exclude_unset=True)
        return FeedbackRepository.update_poll_option(option_id, validated_data)

    @staticmethod
    def remove_poll_option(option_id: str) -> bool:
        """Remove a poll option."""
        return FeedbackRepository.delete_poll_option(option_id)
