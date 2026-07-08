from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes import entry, student, teacher
from models import Base
from database import engine


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(entry.router)
app.include_router(student.router)
app.include_router(teacher.router)

@app.get("/")
def redirect(teacher: bool):
    return RedirectResponse("/docs")
