# app/repositories/feedback_repo.py

from app.db.firebase import db
from datetime import datetime
from typing import List, Dict, Optional

FEEDBACK_QUESTIONS_REF = db.collection("feedback_questions")
POLL_OPTIONS_REF = db.collection("poll_options")
FEEDBACK_RESPONSES_REF = db.collection("feedback_responses")

class FeedbackRepository:

    # Question Management
    @staticmethod
    def get_all_questions() -> List[Dict]:
        """Get all feedback questions"""
        questions = []
        for doc in FEEDBACK_QUESTIONS_REF.order_by("created_at", direction="DESCENDING").stream():
            question_data = doc.to_dict()
            questions.append({
                "id": doc.id,
                "question": question_data.get("question", ""),
                "options": question_data.get("options", []),
                "isActive": question_data.get("is_active", False), # Ensure camelCase for frontend
                "createdAt": question_data.get("created_at").isoformat() if question_data.get("created_at") else "" # Ensure camelCase for frontend
            })
        return questions

    @staticmethod
    def get_active_questions() -> List[Dict]:
        """Get only active feedback questions"""
        questions = []
        for doc in FEEDBACK_QUESTIONS_REF.where("is_active", "==", True).order_by("created_at", direction="DESCENDING").stream():
            question_data = doc.to_dict()
            questions.append({
                "id": doc.id,
                "question": question_data.get("question", ""),
                "options": question_data.get("options", []),
                "isActive": question_data.get("is_active", False), # Ensure camelCase for frontend
                "createdAt": question_data.get("created_at").isoformat() if question_data.get("created_at") else "" # Ensure camelCase for frontend
            })
        return questions

    @staticmethod
    def create_question(question_data: Dict) -> Dict:
        """Create a new feedback question in Firestore."""
        if "created_at" not in question_data:
            question_data["created_at"] = datetime.now()
        if "is_active" not in question_data:
            question_data["is_active"] = True

        doc_ref = FEEDBACK_QUESTIONS_REF.add(question_data)
        # Return the created document's ID and data, ensuring frontend-friendly keys
        return {
            "id": doc_ref[1].id,
            "question": question_data.get("question", ""),
            "options": question_data.get("options", []),
            "isActive": question_data.get("is_active", False), # Ensure camelCase for frontend
            "createdAt": question_data["created_at"].isoformat() # Ensure camelCase for frontend
        }

    @staticmethod
    def get_question_by_id(question_id: str) -> Optional[Dict]:
        """Get a single feedback question by its ID."""
        doc = FEEDBACK_QUESTIONS_REF.document(question_id).get()
        if doc.exists:
            question_data = doc.to_dict()
            return {
                "id": doc.id,
                "question": question_data.get("question", ""),
                "options": question_data.get("options", []),
                "isActive": question_data.get("is_active", False), # Ensure camelCase for frontend
                "createdAt": question_data.get("created_at").isoformat() if question_data.get("created_at") else "" # Ensure camelCase for frontend
            }
        return None

    @staticmethod
    def update_question(question_id: str, update_data: Dict) -> bool:
        """Update an existing feedback question in Firestore."""
        # Convert 'isActive' from frontend to 'is_active' for backend if present
        if 'isActive' in update_data:
            update_data['is_active'] = update_data.pop('isActive')

        # Ensure 'options' is a list if present and not already one (this line might be redundant if Pydantic handles it)
        if 'options' in update_data and not isinstance(update_data['options'], list):
            update_data['options'] = list(update_data['options'])

        FEEDBACK_QUESTIONS_REF.document(question_id).update(update_data)
        return True

    @staticmethod
    def delete_question(question_id: str) -> bool:
        """Delete a feedback question from Firestore."""
        FEEDBACK_QUESTIONS_REF.document(question_id).delete()
        return True

    # Poll Option Management
    @staticmethod
    def create_poll_option(option_data: Dict) -> Dict:
        """Create a new poll option."""
        doc_ref = POLL_OPTIONS_REF.add(option_data)
        return {"id": doc_ref[1].id, **option_data}

    @staticmethod
    def get_poll_options() -> List[Dict]:
        """Get all poll options."""
        options = []
        for doc in POLL_OPTIONS_REF.stream():
            option_data = doc.to_dict()
            options.append({
                "id": doc.id,
                "label": option_data.get("label", ""),
                "minScore": option_data.get("min_score"), # Ensure camelCase for frontend
                "maxScore": option_data.get("max_score"), # Ensure camelCase for frontend
                "requiresContact": option_data.get("requires_contact", False) # Ensure camelCase for frontend
            })
        return options

    @staticmethod
    def update_poll_option(option_id: str, update_data: Dict) -> bool:
        """Update an existing poll option."""
        # Convert frontend keys to backend keys if necessary
        if 'minScore' in update_data:
            update_data['min_score'] = update_data.pop('minScore')
        if 'maxScore' in update_data:
            update_data['max_score'] = update_data.pop('maxScore')
        if 'requiresContact' in update_data:
            update_data['requires_contact'] = update_data.pop('requiresContact')

        POLL_OPTIONS_REF.document(option_id).update(update_data)
        return True

    @staticmethod
    def delete_poll_option(option_id: str) -> bool:
        """Delete a poll option."""
        POLL_OPTIONS_REF.document(option_id).delete()
        return True

    # Feedback Response Management
    @staticmethod
    def create_feedback_response(response_data: Dict) -> str:
        """Create a new feedback response in Firestore."""
        if "submitted_at" not in response_data:
            response_data["submitted_at"] = datetime.now()
        doc_ref = FEEDBACK_RESPONSES_REF.add(response_data)
        return doc_ref[1].id

    @staticmethod
    def get_feedback_responses(limit: int = 100) -> List[Dict]:
        """Get feedback responses."""
        responses = []
        for doc in FEEDBACK_RESPONSES_REF.order_by("submitted_at", direction="DESCENDING").limit(limit).stream():
            response_data = doc.to_dict()
            responses.append({
                "id": doc.id,
                "studentId": response_data.get("student_id", "anonymous"), # Ensure camelCase for frontend
                "studentName": response_data.get("student_name", "Anonymous"), # Ensure camelCase for frontend
                "questionResponses": response_data.get("question_responses", {}), # Ensure camelCase for frontend
                "comment": response_data.get("comment", ""),
                "pollResponse": response_data.get("poll_response", ""), # Ensure camelCase for frontend
                "contactInfo": response_data.get("contact_info"), # Ensure camelCase for frontend
                "language": response_data.get("language", "english"),
                "submittedAt": response_data.get("submitted_at").isoformat() if response_data.get("submitted_at") else "" # Ensure camelCase for frontend
            })
        return responses

    @staticmethod
    def delete_feedback_response(response_id: str) -> bool:
        """Delete a feedback response from Firestore."""
        FEEDBACK_RESPONSES_REF.document(response_id).delete()
        return True

    @staticmethod
    def get_question_statistics() -> List[Dict]:
        """Get question response statistics."""
        questions = FeedbackRepository.get_all_questions()
        responses = FeedbackRepository.get_feedback_responses(limit=1000) # Fetch more responses for better analytics

        question_stats = []
        for question in questions:
            question_id = question["id"]
            question_text = question["question"]
            options = question["options"]

            option_counts = {option: 0 for option in options}
            for response in responses:
                question_responses = response.get("questionResponses", {}) # Use camelCase key
                if question_id in question_responses:
                    selected_option = question_responses[question_id]
                    if selected_option in option_counts:
                        option_counts[selected_option] += 1

            question_stats.append({
                "questionId": question_id, # Ensure camelCase for frontend
                "question": question_text,
                "responses": option_counts
            })

        return question_stats

    @staticmethod
    def get_poll_statistics() -> List[Dict]:
        """Get poll response statistics"""
        poll_options = FeedbackRepository.get_poll_options()
        responses = FeedbackRepository.get_feedback_responses(limit=1000)

        poll_stats = []
        total_responses = len(responses)

        for option in poll_options:
            option_id = option["id"]
            # Ensure 'pollResponse' matches the key used in feedback_responses (camelCase)
            count = sum(1 for response in responses if response.get("pollResponse") == option_id)
            percentage = (count / total_responses * 100) if total_responses > 0 else 0

            poll_stats.append({
                "optionId": option_id, # Ensure camelCase for frontend
                "option": option["label"],
                "count": count,
                "percentage": round(percentage, 1)
            })

        return poll_stats

    @staticmethod
    def get_contact_list_from_responses() -> List[Dict]:
        """Get a list of contact info from responses that required it."""
        contact_list = []
        responses = FeedbackRepository.get_feedback_responses(limit=1000)
        for response in responses:
            if response.get("contactInfo") and response["contactInfo"].get("phoneNumber"): # Use camelCase keys
                contact_list.append({
                    "name": response.get("studentName", "Anonymous"), # Use camelCase key
                    "score": response["contactInfo"].get("score", 0),
                    "phoneNumber": response["contactInfo"].get("phoneNumber", ""), # Use camelCase key
                    "submittedAt": response["submittedAt"] # Use camelCase key
                })
        return contact_list
