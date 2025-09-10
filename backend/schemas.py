from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime

# Helper function to convert comma-separated string to list
def list_from_string(v: Optional[str]) -> List[str]:
    if v is None:
        return []
    if isinstance(v, list):
        return v
    return [item.strip() for item in v.split(',')]

# --- Problem Schemas ---
class ProblemBase(BaseModel):
    source: str
    original_text: str
    subreddit: Optional[str] = None
    author_username: Optional[str] = None
    author_karma: Optional[int] = None
    summary: Optional[str] = None
    category: Optional[str] = None
    score: Optional[int] = 0
    processed: Optional[bool] = False

class ProblemCreate(ProblemBase):
    keywords: Optional[List[str]] = []

class Problem(ProblemBase):
    id: int
    created_at: datetime
    keywords: List[str]

    @field_validator('keywords', mode='before')
    def split_keywords(cls, v):
        return list_from_string(v)

    class Config:
        from_attributes = True

# --- Vote Schemas ---
class VoteBase(BaseModel):
    problem_id: int
    user_identifier: str

class VoteCreate(VoteBase):
    pass

class Vote(VoteBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Entrepreneur Schemas ---
class EntrepreneurBase(BaseModel):
    name: str
    organization: Optional[str] = None
    description: Optional[str] = None
    expertise: List[str] = []

class EntrepreneurCreate(EntrepreneurBase):
    email: str # Email is required for creation, but not for display

class Entrepreneur(EntrepreneurBase):
    id: int
    created_at: datetime

    @field_validator('expertise', mode='before')
    def split_expertise(cls, v):
        return list_from_string(v)

    class Config:
        from_attributes = True

# --- User Submission Schema ---
class UserProblemSubmission(BaseModel):
    text: str
    user: Optional[str] = "anonymous"
