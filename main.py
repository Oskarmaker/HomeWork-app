from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes import entry, student, teacher
from models import Base
from database import engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

Base.metadata.create_all(bind=engine)

app.include_router(entry.router)
app.include_router(student.router)
app.include_router(teacher.router)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
def redirect():
    return RedirectResponse("/docs")
