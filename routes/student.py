from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from models import Teacher, Student, Tasks, TasksStudent
from dependencies import require_student
import os
from schemas import TaskResponse
from fastapi.responses import FileResponse
from utils import build_task_response


router = APIRouter()

@router.get("/student/me/tasks/{number}/file")
def get_file(number: int, db: Session = Depends(get_db), user = Depends(require_student)):
    student = db.query(Student).filter(Student.login == user["login"]).first()
    task = db.query(TasksStudent).filter(TasksStudent.task == number, TasksStudent.student == student.id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.media_url is None:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(task.media_url)

@router.get("/student/me/tasks")
def get_tasks(db: Session = Depends(get_db), user = Depends(require_student)):
    student = db.query(Student).filter(Student.login == user["login"]).first()
    results = db.query(Tasks, TasksStudent, Teacher).join(TasksStudent).join(Teacher, Tasks.creator == Teacher.id).filter(TasksStudent.student == student.id).all()
    ans = []
    for row in results:
        task = row.Tasks
        task_student = row.TasksStudent
        creator = row.Teacher
        ans.append(build_task_response(task, task_student, creator))
    return ans

@router.get("/student/me/tasks/{number}")
def get_task(number: int, db: Session = Depends(get_db), user = Depends(require_student)):
    student = db.query(Student).filter(Student.login == user["login"]).first()
    result = db.query(Tasks, TasksStudent, Teacher).join(TasksStudent).join(Teacher, Tasks.creator == Teacher.id).filter(TasksStudent.student == student.id).filter(Tasks.id == number).first()
    if result is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task = result.Tasks
    task_student = result.TasksStudent
    creator = result.Teacher
    return build_task_response(task, task_student, creator)

@router.post("/student/me/tasks/{number}/load")
async def load_file(number: int, file: UploadFile = File(...), db: Session = Depends(get_db), user = Depends(require_student)):
    student = db.query(Student).filter(Student.login == user["login"]).first()
    contents = await file.read()
    folder = "uploads"
    os.makedirs(folder, exist_ok=True)
    file_path = f"{folder}/task_{number}_{user['login']}{os.path.splitext(file.filename)[1]}"
    with open(file_path, "wb") as f:
        f.write(contents)
    tasks_student = db.query(TasksStudent).filter(TasksStudent.task == number, TasksStudent.student == student.id).first()
    if tasks_student is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if tasks_student.complete:
        raise HTTPException(status_code=409, detail="You cannot change the submitted task")
    tasks_student.media_url = file_path
    db.commit()
    return file_path

@router.post("/student/me/tasks/{number}/send")
def send_task(number: int, db: Session = Depends(get_db), user = Depends(require_student)):
    student = db.query(Student).filter(Student.login == user["login"]).first()
    tasks_student = db.query(TasksStudent).filter(TasksStudent.task == number, TasksStudent.student == student.id).first()
    if tasks_student is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if tasks_student.complete:
        raise HTTPException(status_code=409, detail="You cannot submit a task for third time")
    tasks_student.complete = True
    db.commit()
    return {"message": "Task sent successfully"}
    
