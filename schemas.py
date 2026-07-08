from pydantic import BaseModel 
from datetime import datetime


class LoginData(BaseModel):
    login: str
    password: str


class TaskCreate(BaseModel):
    name: str
    text: str
    deadline: datetime
    media_url: str | None
    students: list[str] #list of student logins


class TaskUpdate(BaseModel):
    name: str | None
    text: str | None
    deadline: datetime | None
    media_url: str | None
    students: list[str] | None #list of student logins
    delete_students: bool = False


class TaskResponse(BaseModel):
    id: int
    name: str
    text: str
    media_url: str | None
    deadline: datetime
    creator: str
    rating: int | None
    comment: str | None
    complete: bool


class StudentResponse(BaseModel):
    student_id: int
    name: str
    surname: str
    patronymic: str | None
    class_name: str
    tasks: int # number of tasks assigned to the student
    comp_tasks: int #number of completed tasks


class RatingTask(BaseModel):
    rating: int
    comment: str | None
