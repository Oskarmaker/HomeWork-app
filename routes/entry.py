from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import verify_password, create_token
from schemas import LoginData
from models import Teacher, Student


router = APIRouter()

@router.post("/student/entry")
def student_entry(data: LoginData, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.login == data.login).first()
    if student is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(data.password, student.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")
    return {"access_token": create_token({"role": "student", "login": data.login}), "token_type": "bearer"}

@router.post("/teacher/entry")
def teacher_entry(data: LoginData, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.login == data.login).first()
    if teacher is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(data.password, teacher.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")
    return {"access_token": create_token({"role": "teacher", "login": data.login}), "token_type": "bearer"}

