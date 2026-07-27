from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Submission, Problem
from schemas import Submission as SubmissionSchema
from auth import get_current_user
import os
import shutil
from config import SUBMISSION_DIR
from judge_service import run_judge

router = APIRouter(prefix="/submissions", tags=["submissions"])

@router.post("/", response_model=SubmissionSchema)
def submit_submission(
    background_tasks: BackgroundTasks,
    problem_id: int = Form(...),
    language: str = Form(...),
    source_code: str = Form(None),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if file:
        if not file.filename.endswith(('.py', '.cpp')):
            raise HTTPException(status_code=400, detail="Invalid file extension")
        source_code = file.file.read().decode('utf-8')
    elif not source_code:
        raise HTTPException(status_code=400, detail="No source code provided")

    if language not in ['python', 'cpp']:
        raise HTTPException(status_code=400, detail="Unsupported language")

    submission = Submission(
        user_id=current_user.id,
        problem_id=problem_id,
        language=language,
        source_code=source_code,
        status="Pending"
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)

    # Chạy chấm bài ngầm
    background_tasks.add_task(run_judge, submission.id)

    return submission

@router.get("/my", response_model=List[SubmissionSchema])
def get_my_submissions(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Submission).filter(Submission.user_id == current_user.id).order_by(Submission.created_at.desc()).all()

@router.get("/{submission_id}", response_model=SubmissionSchema)
def get_submission(submission_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    sub = db.query(Submission).filter(Submission.id == submission_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    if sub.user_id != current_user.id and current_user.role != 'teacher':
        raise HTTPException(status_code=403, detail="Permission denied")
    return sub
