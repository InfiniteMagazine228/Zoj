from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Problem, TestCase
from schemas import Problem as ProblemSchema, ProblemCreate
from auth import get_current_user, get_current_teacher
import os
import shutil
from config import TESTCASE_DIR

router = APIRouter(prefix="/problems", tags=["problems"])

@router.get("/", response_model=List[ProblemSchema])
def get_problems(db: Session = Depends(get_db)):
    return db.query(Problem).all()

@router.get("/{problem_id}", response_model=ProblemSchema)
def get_problem(problem_id: int, db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem

@router.post("/", response_model=ProblemSchema)
def create_problem(
    title: str = Form(...),
    statement: str = Form(...),
    time_limit: int = Form(2),
    memory_limit: int = Form(256),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher)
):
    problem = Problem(title=title, statement=statement, time_limit=time_limit, memory_limit=memory_limit)
    db.add(problem)
    db.commit()
    db.refresh(problem)
    return problem

@router.post("/{problem_id}/testcases")
def upload_testcases(
    problem_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher)
):
    # files chẵn: input, lẻ: output
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    prob_dir = os.path.join(TESTCASE_DIR, str(problem_id))
    os.makedirs(prob_dir, exist_ok=True)
    
    for i in range(0, len(files), 2):
        if i+1 >= len(files): break
        inp_file = files[i]
        out_file = files[i+1]
        
        inp_path = os.path.join(prob_dir, f"{i//2}.in")
        out_path = os.path.join(prob_dir, f"{i//2}.out")
        
        with open(inp_path, "wb") as f: shutil.copyfileobj(inp_file.file, f)
        with open(out_path, "wb") as f: shutil.copyfileobj(out_file.file, f)
        
        tc = TestCase(problem_id=problem_id, input_file=inp_path, output_file=out_path, hidden=True)
        db.add(tc)
    
    db.commit()
    return {"status": "success"}
