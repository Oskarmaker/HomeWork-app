from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes import auth, student, teacher
from models import Base
from database import engine


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(student.router)
app.include_router(teacher.router)

@app.get("/")
def redirect(teacher: bool):
    if teacher:
        return RedirectResponse("/teacher/entry")
    else:
        return RedirectResponse("/student/entry")
    

