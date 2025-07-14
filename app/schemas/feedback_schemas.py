from pydantic import BaseModel, field_validator, ValidationInfo, model_validator # Added model_validator
from typing import Dict, List, Optional
from datetime import datetime
import re

class FeedbackQuestionCreate(BaseModel):
    question: str
    options: List[str]
    admin_id: Optional[str] = "admin"

    @field_validator('options')
    @classmethod
    def validate_options_length(cls, v):
        if len(v) < 2:
            raise ValueError('Must have at least 2 options')
        if len(v) > 6:
            raise ValueError('Cannot have more than 6 options')
        return v

    @field_validator('question')
    @classmethod
    def validate_question_length(cls, v):
        if len(v.strip()) < 10:
            raise ValueError('Question must be at least 10 characters long')
        if len(v.strip()) > 500:
            raise ValueError('Question cannot exceed 500 characters')
        return v.strip()

class FeedbackQuestionUpdate(BaseModel):
    question: Optional[str] = None
    options: Optional[List[str]] = None
    is_active: Optional[bool] = None

    @field_validator('options', mode='after')
    @classmethod
    def validate_options_update_length(cls, v):
        if v is not None:
            if len(v) < 2:
                raise ValueError('Must have at least 2 options')
            if len(v) > 6:
                raise ValueError('Cannot have more than 6 options')
        return v

    @field_validator('question', mode='after')
    @classmethod
    def validate_question_update_length(cls, v):
        if v is not None:
            if len(v.strip()) < 10:
                raise ValueError('Question must be at least 10 characters long')
            if len(v.strip()) > 500:
                raise ValueError('Question cannot exceed 500 characters')
        return v.strip() if v else v

class PollOptionCreate(BaseModel):
    label: str
    min_score: Optional[int] = None
    max_score: Optional[int] = None
    requires_contact: bool = False

    @field_validator('min_score', 'max_score', mode='after')
    @classmethod
    def validate_score_range(cls, v, info: ValidationInfo):
        if v is not None:
            if v < 0 or v > 600:
                raise ValueError(f'{info.field_name} must be between 0 and 600')
        return v

    @field_validator('label')
    @classmethod
    def validate_label_length(cls, v):
        if len(v.strip()) < 3:
            raise ValueError('Label must be at least 3 characters long')
        if len(v.strip()) > 100:
            raise ValueError('Label cannot exceed 100 characters')
        return v.strip()

    @model_validator(mode='after') # Changed to model_validator for cross-field validation
    def validate_max_greater_than_min(self) -> 'PollOptionCreate':
        if self.min_score is not None and self.max_score is not None:
            if self.max_score < self.min_score:
                raise ValueError('max_score cannot be less than min_score')
        return self

class PollOptionUpdate(BaseModel):
    label: Optional[str] = None
    min_score: Optional[int] = None
    max_score: Optional[int] = None
    requires_contact: Optional[bool] = None

    @field_validator('min_score', 'max_score', mode='after')
    @classmethod
    def validate_score_range_update(cls, v, info: ValidationInfo):
        if v is not None:
            if v < 0 or v > 600:
                raise ValueError(f'{info.field_name} must be between 0 and 600')
        return v

    @field_validator('label', mode='after')
    @classmethod
    def validate_label_update_length(cls, v):
        if v is not None:
            if len(v.strip()) < 3:
                raise ValueError('Label must be at least 3 characters long')
            if len(v.strip()) > 100:
                raise ValueError('Label cannot exceed 100 characters')
        return v.strip() if v else v

    @model_validator(mode='after') # Changed to model_validator for cross-field validation
    def validate_max_greater_than_min_update(self) -> 'PollOptionUpdate':
        if self.min_score is not None and self.max_score is not None:
            if self.max_score < self.min_score:
                raise ValueError('max_score cannot be less than min_score')
        return self

class ContactInfo(BaseModel):
    score: int
    phone_number: str

    @field_validator('score')
    @classmethod
    def validate_score(cls, v):
        if v < 0 or v > 600:
            raise ValueError('Score must be between 0 and 600')
        return v

    @field_validator('phone_number')
    @classmethod
    def validate_phone_number_format(cls, v):
        patterns = [
            r'^\+2519\d{8}$',  # +2519XXXXXXXX
            r'^09\d{8}$',      # 09XXXXXXXX
            r'^9\d{8}$'        # 9XXXXXXXX
        ]
        if not any(re.fullmatch(pattern, v.strip()) for pattern in patterns):
            raise ValueError('Invalid Ethiopian phone number format')
        return v.strip()

class FeedbackSubmission(BaseModel):
    student_id: Optional[str] = "anonymous"
    student_name: Optional[str] = "Anonymous"
    question_responses: Dict[str, str]
    comment: Optional[str] = ""
    poll_response: str
    contact_info: Optional[ContactInfo] = None
    language: str = "english"

    @field_validator('language')
    @classmethod
    def validate_language(cls, v):
        if v not in ['english', 'amharic']:
            raise ValueError('Language must be either english or amharic')
        return v

    @field_validator('comment')
    @classmethod
    def validate_comment(cls, v):
        if v and len(v) > 1000:
            raise ValueError('Comment cannot exceed 1000 characters')
        return v.strip() if v else ""

class FeedbackResponse(BaseModel):
    id: str
    student_id: str
    student_name: str
    question_responses: Dict[str, str]
    comment: str
    poll_response: str
    contact_info: Optional[ContactInfo]
    language: str
    submitted_at: datetime

class AnalyticsRequest(BaseModel):
    time_range: str = "all"

    @field_validator('time_range')
    @classmethod
    def validate_time_range(cls, v):
        if v not in ['all', 'day', 'week', 'month', 'year']:
            raise ValueError('Time range must be one of: all, day, week, month, year')
        return v
