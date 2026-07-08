from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from models import Teacher, Student, Tasks, TasksStudent
from dependencies import require_teacher
from sqlalchemy.orm import Session
from schemas import TaskCreate, TaskUpdate, RatingTask


router = APIRouter()

@router.get("/teacher/me/students")
def get_students(db: Session = Depends(get_db), user = Depends(require_teacher)):
    teacher = db.query(Teacher).filter(Teacher.login == user["login"]).first()
    students = db.query(Student).filter(Student.teacher_id == teacher.id).all()
    return students

@router.get("/teacher/me/students/{student_login}/tasks")
def get_student_tasks(student_login: str, db: Session = Depends(get_db), user = Depends(require_teacher)):
    teacher = db.query(Teacher).filter(Teacher.login == user["login"]).first()
    student = db.query(Student).filter(Student.teacher_id == teacher.id, Student.login == student_login).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    results = db.query(Tasks, TasksStudent).join(TasksStudent).filter(TasksStudent.student == student.id).all()
    return results

@router.get("/teacher/me/students/{student_login}/tasks/{number}")
def get_student_task(student_login: str, number: int, db: Session = Depends(get_db), user = Depends(require_teacher)):
    teacher = db.query(Teacher).filter(Teacher.login == user["login"]).first()
    student = db.query(Student).filter(Student.teacher_id == teacher.id, Student.login == student_login).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    result = db.query(Tasks, TasksStudent).join(TasksStudent).filter(TasksStudent.student == student.id, TasksStudent.task == number).first()
    if result is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return result

@router.post("/teacher/me/students/{student_login}/tasks/{number}/rating")
def set_rating(student_login: str, number: int, rating: RatingTask, db: Session = Depends(get_db), user = Depends(require_teacher)):
    teacher = db.query(Teacher).filter(Teacher.login == user["login"]).first()
    student = db.query(Student).filter(Student.teacher_id == teacher.id, Student.login == student_login).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    tasks_student = db.query(TasksStudent).filter(TasksStudent.student == student.id, TasksStudent.task == number).first()
    if tasks_student is None:
        raise HTTPException(status_code=404, detail="Tasks not found")
    tasks_student.rating = rating.rating
    tasks_student.comment = rating.comment
    db.commit()
    return {"message": "rating was successfully completed"}

@router.post("/teacher/me/tasks")
def create_task(data: TaskCreate, db: Session = Depends(get_db), user = Depends(require_teacher)):
    teacher = db.query(Teacher).filter(Teacher.login == user["login"]).first()
    student = db.query(Student).filter(Student.teacher_id == teacher.id).all()
    s_logins = [i.login for i in student]
    data_students = set(s_logins) & set(data.students)
    new_task = Tasks(name=data.name, text=data.text, deadline=data.deadline, creator=teacher.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    for student_login in data_students:
        student_ = db.query(Student).filter(Student.login == student_login).first()
        task_student = TasksStudent(task=new_task.id, student=student_.id, complete=False)  
        db.add(task_student)
    db.commit()
    return {"message": "task was create successfully"}

@router.patch("/teacher/me/tasks/{number}")
def patch_taks(data: TaskUpdate, number: int, db: Session = Depends(get_db), user = Depends(require_teacher)):
    teacher = db.query(Teacher).filter(Teacher.login == user["login"]).first()
    students = db.query(Student).filter(Student.teacher_id == teacher.id).all()
    task = db.query(Tasks).filter(Tasks.id == number, Tasks.creator == teacher.id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if data.deadline is not None:
        task.deadline = data.deadline
    if data.media_url is not None:
        task.media_url = data.media_url
    if data.name is not None:
        task.name = data.name
    if data.text is not None:
        task.text = data.text
    s_logins = [i.login for i in students]
    data_students = set(s_logins) & set(data.students or [])
    if data_students:
        if not data.delete_students:
            for student_login in data_students:
                student_ = db.query(Student).filter(Student.login == student_login).first()
                new_task_student = TasksStudent(task=number, student=student_.id, complete=False)
                db.add(new_task_student)
        else:
            for student_login in data_students:
                student_ = db.query(Student).filter(Student.login == student_login).first()
                task_student = db.query(TasksStudent).filter(TasksStudent.task == task.id, TasksStudent.student == student_.id).first()
                db.delete(task_student)
    db.commit()
    return {"message": "Task changed successefully"}

@router.delete("/teacher/me/tasks/{number}")
def delete_task(number: int, db: Session = Depends(get_db), user = Depends(require_teacher)):
    teacher = db.query(Teacher).filter(Teacher.login == user["login"]).first()
    db.query(TasksStudent).filter(TasksStudent.task == number).delete()
    db.query(Tasks).filter(Tasks.creator == teacher.id, Tasks.id == number).delete()
    db.commit()
    return {"message": "Task was successfully deleted"}
