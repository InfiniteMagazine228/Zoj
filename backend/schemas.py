from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    role: str = "student"

class User(UserBase):
    id: int
    role: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    user_id: int

class ProblemBase(BaseModel):
    title: str
    statement: str
    time_limit: int = 2
    memory_limit: int = 256

class ProblemCreate(ProblemBase):
    pass

class Problem(ProblemBase):
    id: int
    class Config:
        from_attributes = True

class SubmissionBase(BaseModel):
    problem_id: int
    language: str
    source_code: str

class Submission(SubmissionBase):
    id: int
    user_id: int
    score: float
    status: str
    runtime: int
    created_at: datetime
    class Config:
        from_attributes = True
