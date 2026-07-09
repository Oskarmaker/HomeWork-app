from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from models import Teacher, Student, Tasks, TasksStudent
from dependencies import require_student
import os
from schemas import TaskResponse


router = APIRouter()

@router.get("/student/me/tasks")
def get_tasks(db: Session = Depends(get_db), user = Depends(require_student)):
    student = db.query(Student).filter(Student.login == user["login"]).first()
    results = db.query(Tasks, TasksStudent, Teacher).join(TasksStudent).join(Teacher, Tasks.creator == Teacher.id).filter(TasksStudent.student == student.id).all()
    ans = []
    for row in results:
        task = row.Tasks
        task_student = row.TasksStudent
        creator = row.Teacher
        ans.append(TaskResponse(id=task.id, name=task.name, text=task.text, answer_media=task_student.media_url, task_media=task.media_url, deadline=task.deadline, creator=f"{creator.surname} {creator.name} {creator.patronymic or ''}", rating=task_student.rating, comment=task_student.comment, complete=task_student.complete))
    return ans

@router.get("/student/me/tasks/{number}")
def get_task(number: int, db: Session = Depends(get_db), user = Depends(require_student)):
    student = db.query(Student).filter(Student.login == user["login"]).first()
    result = db.query(Tasks, TasksStudent).join(TasksStudent).filter(TasksStudent.student == student.id).filter(Tasks.id == number).first()
    if result is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return result

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
    tasks_student.media_url = file_path
    db.commit()
    return file_path

@router.post("/student/me/tasks/{number}/send")
def send_task(number: int, db: Session = Depends(get_db), user = Depends(require_student)):
    student = db.query(Student).filter(Student.login == user["login"]).first()
    tasks_student = db.query(TasksStudent).filter(TasksStudent.task == number, TasksStudent.student == student.id).first()
    if tasks_student is None:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks_student.complete = True
    db.commit()
    return {"message": "Task sent successfully"}
    
