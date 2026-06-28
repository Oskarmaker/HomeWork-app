from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey 
from datetime import datetime


class Base(DeclarativeBase):
    pass

class Teacher(Base):
    __tablename__ = "teacher"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)
    patronymic: Mapped[str | None]
    login: Mapped[str] = mapped_column(nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)

class Student(Base):
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)
    patronymic: Mapped[str | None]
    login: Mapped[str] = mapped_column(nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    class_name: Mapped[str] = mapped_column(nullable=False)

class Tasks(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)
    media_url: Mapped[str | None]
    deadline: Mapped[datetime] = mapped_column(nullable=False)
    creator: Mapped[int] = mapped_column(ForeignKey("teacher.id"), nullable=False)

class TasksStudent(Base):
    __tablename__ = "tasks_student"

    task: Mapped[int] = mapped_column(ForeignKey("tasks.id"), primary_key=True)
    student: Mapped[int] = mapped_column(ForeignKey("student.id"), primary_key=True)
    rating: Mapped[int | None]
    comment: Mapped[str | None]
    complete: Mapped[bool] = mapped_column(nullable=False, default=False)