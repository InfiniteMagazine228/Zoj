from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String) # 'teacher' or 'student'
    submissions = relationship("Submission", back_populates="user")

class Problem(Base):
    __tablename__ = "problems"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    statement = Column(Text)
    time_limit = Column(Integer) # seconds
    memory_limit = Column(Integer) # MB
    test_cases = relationship("TestCase", back_populates="problem", cascade="all, delete-orphan")
    submissions = relationship("Submission", back_populates="problem")

class TestCase(Base):
    __tablename__ = "testcases"
    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"))
    input_file = Column(String) # Path to input file
    output_file = Column(String) # Path to output file
    hidden = Column(Boolean, default=True)
    problem = relationship("Problem", back_populates="test_cases")

class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    problem_id = Column(Integer, ForeignKey("problems.id"))
    language = Column(String) # 'python' or 'cpp'
    source_code = Column(Text)
    score = Column(Float, default=0.0)
    status = Column(String, default="Pending")
    runtime = Column(Integer, default=0) # ms
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="submissions")
    problem = relationship("Problem", back_populates="submissions")
